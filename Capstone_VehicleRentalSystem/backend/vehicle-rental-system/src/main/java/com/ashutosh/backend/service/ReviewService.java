package com.ashutosh.backend.service;

import com.ashutosh.backend.dto.request.ReviewRequestDTO;
import com.ashutosh.backend.dto.response.ReviewResponseDTO;
import com.ashutosh.backend.entity.AppUser;
import com.ashutosh.backend.entity.Booking;
import com.ashutosh.backend.entity.Review;
import com.ashutosh.backend.enums.BookingStatus;
import com.ashutosh.backend.exception.DuplicateResourceException;
import com.ashutosh.backend.exception.ResourceNotFoundException;
import com.ashutosh.backend.repository.AppUserRepository;
import com.ashutosh.backend.repository.BookingRepository;
import com.ashutosh.backend.repository.ReviewRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

/**
 * Service class responsible for managing the customer review system.
 * Handles the creation, retrieval, and authorized deletion of vehicle reviews.
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class ReviewService {

    private final ReviewRepository reviewRepository;
    private final BookingRepository bookingRepository;
    private final AppUserRepository appuserRepository;

    /**
     * Facilitates the creation of a new review for a completed trip.
     * Enforces validation rules ensuring users can only review their own bookings,
     * trips must be in a COMPLETED state, and duplicate reviews are prevented.
     *
     * @param request The review details (rating and comment) provided by the user.
     * @param userEmail The email of the currently authenticated user.
     * @return ReviewResponseDTO The persisted review details.
     */
    @Transactional
    public ReviewResponseDTO addReview(ReviewRequestDTO request, String userEmail) {
        log.info("User {} is attempting to add a review for booking ID: {}", userEmail, request.getBookingId());

        Booking booking = bookingRepository.findById(request.getBookingId())
                .orElseThrow(() -> {
                    log.error("Review failed: Booking ID {} not found in the database.", request.getBookingId());
                    return new ResourceNotFoundException("Booking not found");
                });

        // Security check: Ensure the user actually owns this booking
        if (!booking.getUser().getEmail().equals(userEmail)) {
            log.warn("Review rejected: User {} tried to review someone else's booking (ID: {}).", userEmail, booking.getId());
            throw new SecurityException("You can only review your own bookings.");
        }

        // Logic check: Ensure the trip is actually over
        if (booking.getStatus() != BookingStatus.COMPLETED) {
            log.warn("Review rejected: Booking ID {} is not COMPLETED yet.", booking.getId());
            throw new IllegalStateException("Reviews can only be submitted for completed trips.");
        }

        // Logic check: Prevent multiple reviews for the same trip
        if (reviewRepository.existsByBookingId(booking.getId())) {
            log.warn("Review rejected: A review already exists for booking ID {}.", booking.getId());
            throw new DuplicateResourceException("A review has already been submitted for this booking.");
        }

        // Build and save the review entity
        Review review = Review.builder()
                .booking(booking)
                .rating(request.getRating())
                .comment(request.getComment())
                .build();

        Review savedReview = reviewRepository.save(review);
        log.info("Successfully added review ID {} for booking ID {}", savedReview.getId(), booking.getId());

        return mapToResponseDTO(savedReview);
    }

    /**
     * Retrieves all reviews associated with a specific vehicle,
     * ordered by creation date in descending order.
     *
     * @param vehicleId The unique identifier of the vehicle.
     * @return List of ReviewResponseDTOs representing the vehicle's review history.
     */
    @Transactional(readOnly = true)
    public List<ReviewResponseDTO> getVehicleReviews(Long vehicleId) {
        log.info("Fetching all reviews for vehicle ID: {}", vehicleId);

        return reviewRepository.findByBooking_Vehicle_IdOrderByCreatedAtDesc(vehicleId)
                .stream()
                .map(this::mapToResponseDTO)
                .collect(Collectors.toList());
    }

    /**
     * Processes the deletion of a review.
     * Enforces role-based access control, allowing standard users to delete
     * only their own reviews, while granting administrators the authority to delete any review.
     *
     * @param reviewId The unique identifier of the review to delete.
     * @param userEmail The email of the user attempting the deletion.
     */
    @Transactional
    public void deleteReview(Long reviewId, String userEmail) {
        log.info("User {} is attempting to delete review ID: {}", userEmail, reviewId);

        Review review = reviewRepository.findById(reviewId)
                .orElseThrow(() -> {
                    log.error("Delete failed: Review ID {} not found.", reviewId);
                    return new ResourceNotFoundException("Review not found with ID: " + reviewId);
                });

        AppUser user = appuserRepository.findByEmail(userEmail)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        // Check the user's role and ownership
        boolean isAdmin = user.getRole().name().equals("ADMIN");
        boolean isAuthor = review.getBooking().getUser().getId().equals(user.getId());

        if (!isAuthor && !isAdmin) {
            log.warn("Delete rejected: User {} is neither an ADMIN nor the author of review ID {}.", userEmail, reviewId);
            throw new SecurityException("You do not have permission to delete this review.");
        }

        reviewRepository.delete(review);
        log.info("Successfully deleted review ID: {}", reviewId);
    }

    /**
     * Maps a Review database entity to its corresponding Data Transfer Object (DTO).
     * Extracts relevant user details (first name and email) for frontend display purposes.
     *
     * @param review The source database entity.
     * @return ReviewResponseDTO The formatted response object.
     */
    private ReviewResponseDTO mapToResponseDTO(Review review) {
        return ReviewResponseDTO.builder()
                .id(review.getId())
                .bookingId(review.getBooking().getId())
                .rating(review.getRating())
                .comment(review.getComment())
                .reviewerFirstName(review.getBooking().getUser().getFirstName())
                .reviewerEmail(review.getBooking().getUser().getEmail())
                .createdAt(review.getCreatedAt())
                .build();
    }
}