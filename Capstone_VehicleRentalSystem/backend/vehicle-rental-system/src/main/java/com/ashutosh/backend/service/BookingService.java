package com.ashutosh.backend.service;

import com.ashutosh.backend.dto.request.BookingRequestDTO;
import com.ashutosh.backend.dto.response.BookingResponseDTO;
import com.ashutosh.backend.entity.AppUser;
import com.ashutosh.backend.entity.Booking;
import com.ashutosh.backend.entity.Vehicle;
import com.ashutosh.backend.enums.BookingStatus;
import com.ashutosh.backend.enums.VehicleStatus;
import com.ashutosh.backend.exception.ResourceNotFoundException;
import com.ashutosh.backend.repository.AppUserRepository;
import com.ashutosh.backend.repository.BookingRepository;
import com.ashutosh.backend.repository.VehicleRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Service class responsible for managing the lifecycle of vehicle bookings.
 * Handles scheduling, cancellations, status evaluations, and overlap validations.
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class BookingService {

    private final BookingRepository bookingRepository;
    private final VehicleRepository vehicleRepository;
    private final AppUserRepository appuserRepository;
    private final com.ashutosh.backend.repository.ReviewRepository reviewRepository;

    /**
     * Validates and processes a new vehicle rental request.
     * Ensures dates are logical, duration constraints are met, and the vehicle
     * is not double-booked for the requested time frame.
     *
     * @param request The requested booking parameters from the user.
     * @param userEmail The email of the currently authenticated user making the request.
     * @return BookingResponseDTO The details of the newly confirmed booking.
     */
    @Transactional
    public BookingResponseDTO createBooking(BookingRequestDTO request, String userEmail) {
        log.info("Attempting to create a booking for user: {} and vehicle ID: {}", userEmail, request.getVehicleId());

        // Validate dates
        if (request.getEndDate().isBefore(request.getStartDate())) {
            log.warn("Booking failed: End date is before start date.");
            throw new IllegalArgumentException("End date cannot be before start date.");
        }

        LocalDate maxAdvanceDate = LocalDate.now().plusMonths(3);
        if (request.getStartDate().isAfter(maxAdvanceDate)) {
            log.warn("Booking failed: Requested start date exceeds the 3-month advance limit.");
            throw new IllegalArgumentException("Bookings can only be made up to 3 months in advance.");
        }

        long days = ChronoUnit.DAYS.between(request.getStartDate(), request.getEndDate()) + 1;
        if (days > 30) {
            log.warn("Booking failed: Rental duration of {} days exceeds the 30-day maximum.", days);
            throw new IllegalArgumentException("Maximum rental duration cannot exceed 30 days.");
        }

        AppUser user = appuserRepository.findByEmail(userEmail)
                .orElseThrow(() -> {
                    log.error("Booking creation failed: User {} not found.", userEmail);
                    return new RuntimeException("User not found");
                });

        Vehicle vehicle = vehicleRepository.findById(request.getVehicleId())
                .orElseThrow(() -> {
                    log.error("Booking creation failed: Vehicle ID {} not found.", request.getVehicleId());
                    return new RuntimeException("Vehicle not found");
                });

        if (vehicle.getStatus() != VehicleStatus.AVAILABLE) {
            log.warn("Booking failed: Vehicle ID {} is marked as {}.", vehicle.getId(), vehicle.getStatus());
            throw new IllegalStateException("This vehicle is no longer available for new bookings.");
        }

        // Check for Overlaps using custom JPQL Query
        List<Booking> conflicts = bookingRepository.findConflictingBookings(
                vehicle.getId(), request.getStartDate(), request.getEndDate());
        if (!conflicts.isEmpty()) {
            log.warn("Booking failed: Vehicle ID {} is already booked during the requested dates.", vehicle.getId());
            throw new IllegalStateException("Vehicle is already booked during these dates.");
        }

        BigDecimal dailyRate = vehicle.getDailyRate();
        BigDecimal totalAmount = dailyRate.multiply(BigDecimal.valueOf(days));

        // Build and Save
        Booking booking = Booking.builder()
                .user(user)
                .vehicle(vehicle)
                .startDate(request.getStartDate())
                .endDate(request.getEndDate())
                .pricePerDay(dailyRate)
                .totalAmount(totalAmount)
                .status(BookingStatus.CONFIRMED)
                .build();

        Booking savedBooking = bookingRepository.save(booking);
        log.info("Successfully created booking ID: {} for user: {}", savedBooking.getId(), userEmail);

        return mapToResponseDTO(savedBooking);
    }

    /**
     * Retrieves the booking history for a specific user.
     * Evaluates and updates the state of active/completed trips before returning data.
     *
     * @param userEmail The email of the user whose bookings are being retrieved.
     * @return List of the user's booking history.
     */
    @Transactional
    public List<BookingResponseDTO> getUserBookings(String userEmail) {
        log.info("Fetching booking history for user: {}", userEmail);

        AppUser user = appuserRepository.findByEmail(userEmail)
                .orElseThrow(() -> new RuntimeException("User not found"));

        List<Booking> bookings = bookingRepository.findByUser_IdOrderByCreatedAtDesc(user.getId());
        evaluateBookings(bookings);

        return bookings.stream()
                .map(this::mapToResponseDTO)
                .collect(Collectors.toList());
    }

    /**
     * Retrieves the entire system's booking history for administrative oversight.
     * Automatically evaluates states to ensure the dashboard reflects real-time data.
     *
     * @return List of all platform bookings.
     */
    @Transactional
    public List<BookingResponseDTO> getAllBookingsForAdmin() {
        log.info("Admin request: Fetching all system bookings.");

        List<Booking> bookings = bookingRepository.findAllByOrderByCreatedAtDesc();
        evaluateBookings(bookings);

        return bookings.stream()
                .map(this::mapToResponseDTO)
                .collect(Collectors.toList());
    }

    /**
     * Processes a cancellation request for an existing booking.
     * Enforces strict role-based access and prevents cancellation of ongoing trips.
     *
     * @param bookingId The unique identifier of the booking to cancel.
     * @param userEmail The email of the user initiating the cancellation.
     * @return BookingResponseDTO The updated booking status.
     */
    @Transactional
    public BookingResponseDTO cancelBooking(Long bookingId, String userEmail) {
        log.info("Attempting to cancel booking ID: {} requested by: {}", bookingId, userEmail);

        Booking booking = bookingRepository.findById(bookingId)
                .orElseThrow(() -> {
                    log.error("Cancellation failed: Booking ID {} not found.", bookingId);
                    return new ResourceNotFoundException("Booking not found");
                });

        AppUser user = appuserRepository.findByEmail(userEmail)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        boolean isAdmin = user.getRole().name().equals("ADMIN");

        if (!booking.getUser().getId().equals(user.getId()) && !isAdmin) {
            log.warn("Cancellation rejected: User {} does not own booking ID {}.", userEmail, bookingId);
            throw new SecurityException("You do not have permission to cancel this booking.");
        }

        if (booking.getStatus() == BookingStatus.CANCELLED || booking.getStatus() == BookingStatus.COMPLETED) {
            log.warn("Cancellation rejected: Booking ID {} is already in {} state.", bookingId, booking.getStatus());
            throw new IllegalStateException("Booking cannot be cancelled in its current state.");
        }

        if (booking.getStatus() == BookingStatus.ACTIVE) {
            log.warn("Cancellation rejected: Booking ID {} is currently ACTIVE on the road.", bookingId);
            throw new IllegalStateException("Cannot cancel an active, ongoing booking. Vehicle is currently on the road.");
        }

        if (LocalDate.now().isAfter(booking.getStartDate()) || LocalDate.now().isEqual(booking.getStartDate())) {
            log.warn("Cancellation rejected: Start date for Booking ID {} has already passed or is today.", bookingId);
            throw new IllegalStateException("Bookings cannot be cancelled on or after the start date.");
        }

        booking.setStatus(BookingStatus.CANCELLED);
        Booking updatedBooking = bookingRepository.save(booking);

        log.info("Successfully cancelled booking ID: {}", bookingId);
        return mapToResponseDTO(updatedBooking);
    }

    /**
     * Allows an Administrator to manually mark a booking as completed upon vehicle return.
     *
     * @param bookingId The ID of the booking to finalize.
     * @return BookingResponseDTO The finalized booking data.
     */
    @Transactional
    public BookingResponseDTO completeBooking(Long bookingId) {
        log.info("Attempting to manually complete booking ID: {}", bookingId);

        Booking booking = bookingRepository.findById(bookingId)
                .orElseThrow(() -> {
                    log.error("Completion failed: Booking ID {} not found.", bookingId);
                    return new ResourceNotFoundException("Booking not found");
                });

        if (booking.getStatus() != BookingStatus.CONFIRMED && booking.getStatus() != BookingStatus.ACTIVE) {
            log.warn("Completion rejected: Booking ID {} is currently in {} state.", bookingId, booking.getStatus());
            throw new IllegalStateException("Only confirmed or active bookings can be marked as completed.");
        }

        booking.setStatus(BookingStatus.COMPLETED);
        Booking updatedBooking = bookingRepository.save(booking);

        log.info("Successfully marked booking ID: {} as COMPLETED", bookingId);
        return mapToResponseDTO(updatedBooking);
    }

    /**
     * Helper method to lazy-evaluate and transition booking states based on the current date.
     * Transitions CONFIRMED bookings to ACTIVE, and ACTIVE bookings to COMPLETED.
     *
     * @param bookings The list of bookings to evaluate.
     */
    private void evaluateBookings(List<Booking> bookings) {
        log.info("Evaluating booking statuses against current date to update ACTIVE/COMPLETED states.");
        LocalDate today = LocalDate.now();
        boolean dbNeedsUpdate = false;

        for (Booking booking : bookings) {
            if (booking.getStatus() == BookingStatus.CONFIRMED &&
                    !today.isBefore(booking.getStartDate()) &&  // Today is on or after Start Date
                    !today.isAfter(booking.getEndDate())) {     // Today is on or before End Date

                booking.setStatus(BookingStatus.ACTIVE);
                dbNeedsUpdate = true;
            } else if ((booking.getStatus() == BookingStatus.CONFIRMED || booking.getStatus() == BookingStatus.ACTIVE) &&
                    today.isAfter(booking.getEndDate())) {

                booking.setStatus(BookingStatus.COMPLETED);

                Vehicle vehicle = booking.getVehicle();
                if (vehicle.getStatus() == VehicleStatus.BOOKED) {
                    vehicle.setStatus(VehicleStatus.AVAILABLE);
                }

                dbNeedsUpdate = true;
            }
        }

        if (dbNeedsUpdate) {
            bookingRepository.saveAll(bookings);
            log.info("Booking evaluation triggered database updates for state transitions.");
        }
    }

    /**
     * Maps a Booking entity to its corresponding Data Transfer Object.
     * Incorporates nested user and vehicle data, and checks if a review has been left.
     *
     * @param booking The source database entity.
     * @return BookingResponseDTO The formatted response.
     */
    private BookingResponseDTO mapToResponseDTO(Booking booking) {
        return BookingResponseDTO.builder()
                .id(booking.getId())
                .userId(booking.getUser().getId())
                .userName(booking.getUser().getFirstName() + " " + booking.getUser().getLastName())
                .userEmail(booking.getUser().getEmail())
                .vehicleId(booking.getVehicle().getId())
                .vehicleName(booking.getVehicle().getMake() + " " + booking.getVehicle().getModel())
                .vehicleType(booking.getVehicle().getVehicleType())
                .vehicleMake(booking.getVehicle().getMake())
                .vehicleModel(booking.getVehicle().getModel())
                .startDate(booking.getStartDate())
                .endDate(booking.getEndDate())
                .totalAmount(booking.getTotalAmount())
                .status(booking.getStatus())
                .createdAt(booking.getCreatedAt())
                .isReviewed(reviewRepository.existsByBookingId(booking.getId()))
                .build();
    }
}