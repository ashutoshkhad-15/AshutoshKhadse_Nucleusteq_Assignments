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
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class ReviewService {

    private final ReviewRepository reviewRepository;
    private final BookingRepository bookingRepository;
    private final AppUserRepository appuserRepository;

    @Transactional
    public ReviewResponseDTO addReview(ReviewRequestDTO request, String userEmail) {

        Booking booking = bookingRepository.findById(request.getBookingId())
                .orElseThrow(() -> new ResourceNotFoundException("Booking not found"));

        if (!booking.getUser().getEmail().equals(userEmail)) {
            throw new SecurityException("You can only review your own bookings.");
        }

        if (booking.getStatus() != BookingStatus.COMPLETED) {
            throw new IllegalStateException("Reviews can only be submitted for completed trips.");
        }

        if (reviewRepository.existsByBookingId(booking.getId())) {
            throw new DuplicateResourceException("A review has already been submitted for this booking.");
        }

        Review review = Review.builder()
                .booking(booking)
                .rating(request.getRating())
                .comment(request.getComment())
                .build();

        Review savedReview = reviewRepository.save(review);

        return mapToResponseDTO(savedReview);
    }

    @Transactional(readOnly = true)
    public List<ReviewResponseDTO> getVehicleReviews(Long vehicleId) {
        return reviewRepository.findByBooking_Vehicle_IdOrderByCreatedAtDesc(vehicleId)
                .stream()
                .map(this::mapToResponseDTO)
                .collect(Collectors.toList());
    }

    @Transactional
    public void deleteReview(Long reviewId, String userEmail) {
        Review review = reviewRepository.findById(reviewId)
                .orElseThrow(() -> new ResourceNotFoundException("Review not found with ID: " + reviewId));

        AppUser user = appuserRepository.findByEmail(userEmail)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        boolean isAdmin = user.getRole().name().equals("ADMIN");
        boolean isAuthor = review.getBooking().getUser().getId().equals(user.getId());

        if (!isAuthor && !isAdmin) {
            throw new SecurityException("You do not have permission to delete this review.");
        }

        reviewRepository.delete(review);
    }

    // HELPER METHOD: Entity to DTO Mapper
    private ReviewResponseDTO mapToResponseDTO(Review review) {
        return ReviewResponseDTO.builder()
                .id(review.getId())
                .bookingId(review.getBooking().getId())
                .rating(review.getRating())
                .comment(review.getComment())
                // Extracts the first name from the nested AppUser for the public UI
                .reviewerFirstName(review.getBooking().getUser().getFirstName())
                .createdAt(review.getCreatedAt())
                .build();
    }
}