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
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class BookingService {

    private final BookingRepository bookingRepository;
    private final VehicleRepository vehicleRepository;
    private final AppUserRepository appuserRepository;

    private final com.ashutosh.backend.repository.ReviewRepository reviewRepository;

    @Transactional
    public BookingResponseDTO createBooking(BookingRequestDTO request, String userEmail) {
        // Validate dates
        if (request.getEndDate().isBefore(request.getStartDate())) {
            throw new IllegalArgumentException("End date cannot be before start date.");
        }

        LocalDate maxAdvanceDate = LocalDate.now().plusMonths(3);
        if (request.getStartDate().isAfter(maxAdvanceDate)) {
            throw new IllegalArgumentException("Bookings can only be made up to 3 months in advance.");
        }

        long days = ChronoUnit.DAYS.between(request.getStartDate(), request.getEndDate()) + 1;
        if (days > 30) {
            throw new IllegalArgumentException("Maximum rental duration cannot exceed 30 days.");
        }

        AppUser user = appuserRepository.findByEmail(userEmail)
                .orElseThrow(() -> new RuntimeException("User not found"));
        Vehicle vehicle = vehicleRepository.findById(request.getVehicleId())
                .orElseThrow(() -> new RuntimeException("Vehicle not found"));

        if (vehicle.getStatus() != VehicleStatus.AVAILABLE) {
            throw new IllegalStateException("This vehicle is no longer available for new bookings.");
        }

        // Check for Overlaps using your custom JPQL Query
        List<Booking> conflicts = bookingRepository.findConflictingBookings(
                vehicle.getId(), request.getStartDate(), request.getEndDate());
        if (!conflicts.isEmpty()) {
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

        return mapToResponseDTO(savedBooking);
    }

    @Transactional
    public List<BookingResponseDTO> getUserBookings(String userEmail) {
        AppUser user = appuserRepository.findByEmail(userEmail)
                .orElseThrow(() -> new RuntimeException("User not found"));
        List<Booking> bookings = bookingRepository.findByUser_IdOrderByCreatedAtDesc(user.getId());
        EvaluateBookings(bookings);

        return bookings.stream()
                .map(this::mapToResponseDTO)
                .collect(Collectors.toList());
    }

    @Transactional
    public List<BookingResponseDTO> getAllBookingsForAdmin() {
        List<Booking> bookings = bookingRepository.findAllByOrderByCreatedAtDesc();
        EvaluateBookings(bookings);

        return bookings.stream()
                .map(this::mapToResponseDTO)
                .collect(Collectors.toList());
    }

    @Transactional
    public BookingResponseDTO cancelBooking(Long bookingId, String userEmail) {
        Booking booking = bookingRepository.findById(bookingId)
                .orElseThrow(() -> new ResourceNotFoundException("Booking not found"));

        AppUser user = appuserRepository.findByEmail(userEmail)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        boolean isAdmin = user.getRole().name().equals("ADMIN");

        if (!booking.getUser().getId().equals(user.getId()) && !isAdmin) {
            throw new SecurityException("You do not have permission to cancel this booking.");
        }

        if (booking.getStatus() == BookingStatus.CANCELLED || booking.getStatus() == BookingStatus.COMPLETED) {
            throw new IllegalStateException("Booking cannot be cancelled in its current state.");
        }

        if (LocalDate.now().isAfter(booking.getStartDate()) || LocalDate.now().isEqual(booking.getStartDate())) {
            throw new IllegalStateException("Bookings cannot be cancelled on or after the start date.");
        }

        booking.setStatus(BookingStatus.CANCELLED);
        Booking updatedBooking = bookingRepository.save(booking);

        return mapToResponseDTO(updatedBooking);
    }

    @Transactional
    public BookingResponseDTO completeBooking(Long bookingId) {
        Booking booking = bookingRepository.findById(bookingId)
                .orElseThrow(() -> new ResourceNotFoundException("Booking not found"));

        if (booking.getStatus() != BookingStatus.CONFIRMED) {
            throw new IllegalStateException("Only confirmed bookings can be marked as completed.");
        }

        booking.setStatus(BookingStatus.COMPLETED);
        Booking updatedBooking = bookingRepository.save(booking);

        return mapToResponseDTO(updatedBooking);
    }

    private void EvaluateBookings(List<Booking> bookings) {
        LocalDate today = LocalDate.now();
        boolean dbNeedsUpdate = false;

        for (Booking booking : bookings) {
            if (booking.getStatus() == BookingStatus.CONFIRMED && booking.getEndDate().isBefore(today)) {

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
        }
    }

    // HELPER MAPPER
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