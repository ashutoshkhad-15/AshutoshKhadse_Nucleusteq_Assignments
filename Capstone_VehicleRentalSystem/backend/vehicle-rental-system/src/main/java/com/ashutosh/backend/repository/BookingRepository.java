package com.ashutosh.backend.repository;

import com.ashutosh.backend.entity.Booking;
import com.ashutosh.backend.enums.BookingStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.time.LocalDate;
import java.util.List;

/**
 * Repository interface for managing Booking entities.
 * Handles database operations for rental history, administrative tracking,
 * and critical availability validations.
 */
@Repository
public interface BookingRepository extends JpaRepository<Booking, Long> {

    /**
     * Retrieves all bookings for a specific user.
     * Sorts the results by creation date in descending order to show the latest activity first.
     *
     * @param userId The unique identifier of the user.
     * @return A list of the user's booking history.
     */
    List<Booking> findByUser_IdOrderByCreatedAtDesc(Long userId);

    /**
     * Retrieves every booking in the system for administrative oversight.
     * Organizes the records by the most recently created to facilitate dashboard monitoring.
     *
     * @return A comprehensive list of all system bookings.
     */
    List<Booking> findAllByOrderByCreatedAtDesc();

    /**
     * Identifies any existing bookings that overlap with a requested time frame.
     * Uses a specific date-logic check to find conflicts. It ignores cancelled bookings
     * to ensure that only valid, active, or pending reservations block new requests.
     *
     * @param vehicleId The ID of the vehicle being checked.
     * @param startDate The start of the requested rental period.
     * @param endDate The end of the requested rental period.
     * @return A list of conflicting booking records found in the database.
     */
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

    /**
     * Filters bookings for a specific vehicle based on their current status.
     * Primarily used to audit a vehicle's current activity or usage history.
     *
     * @param vehicleId The ID of the target vehicle.
     * @param status The status to filter by (e.g., ACTIVE, COMPLETED).
     * @return A list of matching booking records.
     */
    List<Booking> findByVehicle_IdAndStatus(Long vehicleId, BookingStatus status);

}