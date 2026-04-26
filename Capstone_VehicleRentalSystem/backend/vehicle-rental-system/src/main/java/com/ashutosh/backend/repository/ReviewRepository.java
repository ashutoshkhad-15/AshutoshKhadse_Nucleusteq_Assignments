package com.ashutosh.backend.repository;

import com.ashutosh.backend.entity.Review;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ReviewRepository extends JpaRepository<Review, Long> {

    boolean existsByBookingId(Long bookingId);
    
    List<Review> findByBooking_Vehicle_IdOrderByCreatedAtDesc(Long vehicleId);
}