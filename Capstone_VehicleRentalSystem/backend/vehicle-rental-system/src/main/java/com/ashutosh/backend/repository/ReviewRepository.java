package com.ashutosh.backend.repository;

import com.ashutosh.backend.entity.Review;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ReviewRepository extends JpaRepository<Review, Long> {
    // this allows us to pull up a review based on the specific booking ID.
    boolean existsByBookingId(Long bookingId);
}