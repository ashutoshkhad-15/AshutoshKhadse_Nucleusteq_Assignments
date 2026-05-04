package com.ashutosh.backend.repository;

import com.ashutosh.backend.entity.Review;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repository interface for managing customer reviews.
 * Handles database operations for checking feedback status and retrieving vehicle ratings.
 */
@Repository
public interface ReviewRepository extends JpaRepository<Review, Long> {

    /**
     * Checks if a review has already been submitted for a specific booking.
     * Used to prevent duplicate reviews for the same rental transaction.
     *
     * @param bookingId The unique identifier of the booking.
     * @return True if a review exists, false otherwise.
     */
    boolean existsByBookingId(Long bookingId);

    /**
     * Retrieves all reviews for a specific vehicle.
     * Organizes the feedback by the most recent date to provide up-to-date insights for users.
     *
     * @param vehicleId The unique identifier of the vehicle.
     * @return A list of reviews associated with the vehicle, sorted by newest first.
     */
    List<Review> findByBooking_Vehicle_IdOrderByCreatedAtDesc(Long vehicleId);
}