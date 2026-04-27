package com.ashutosh.backend.repository;

import com.ashutosh.backend.entity.Booking;
import com.ashutosh.backend.enums.BookingStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.time.LocalDate;
import java.util.List;

@Repository
public interface BookingRepository extends JpaRepository<Booking, Long> {
    // this will be used for the User Dashboard so they can see their booking history (sorted newest first)
    List<Booking> findByUser_IdOrderByCreatedAtDesc(Long userId);

    // Admin dashboard (sorted newest first)
    List<Booking> findAllByOrderByCreatedAtDesc();

    // combining Java 17 text blocks for readability with COUNT for performance.
    // We check for any status EXCEPT 'CANCELLED' to ensure 'PENDING' bookings also block new reservations,
    // preventing race-condition double-bookings.
    @Query("""
        SELECT b FROM Booking b
        WHERE b.vehicle.id = :vehicleId
        AND b.status != 'CANCELLED'
        AND b.startDate <= :endDate
        AND b.endDate >= :startDate
    """)
    List<Booking> findConflictingBookings(
            @Param("vehicleId") Long vehicleId,
            @Param("startDate") LocalDate startDate,
            @Param("endDate") LocalDate endDate
    );

    // checks active bookings for vehicle
    List<Booking> findByVehicle_IdAndStatus(Long vehicleId, BookingStatus status);

}