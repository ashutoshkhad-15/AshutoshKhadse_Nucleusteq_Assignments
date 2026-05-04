package com.ashutosh.backend.repository;

import com.ashutosh.backend.entity.Vehicle;
import com.ashutosh.backend.enums.VehicleStatus;
import com.ashutosh.backend.enums.VehicleType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;

/**
 * Repository interface for managing vehicle inventory.
 * Provides methods for filtering the fleet by status, type, and specific availability dates.
 */
@Repository
public interface VehicleRepository extends JpaRepository<Vehicle, Long> {

    /**
     * Retrieves a list of vehicles based on their current operational status.
     *
     * @param status The status to filter by, such as AVAILABLE or BOOKED.
     * @return A list of matching vehicles.
     */
    List<Vehicle> findByStatus(VehicleStatus status);

    /**
     * Filters the inventory by both vehicle category and current status.
     *
     * @param type The type of vehicle (e.g., CAR, BIKE).
     * @param status The current availability status.
     * @return A list of vehicles matching both criteria.
     */
    List<Vehicle> findByVehicleTypeAndStatus(VehicleType type, VehicleStatus status);

    /**
     * Retrieves all vehicles belonging to a specific category.
     *
     * @param vehicleType The type of vehicle to search for.
     * @return A list of vehicles of the specified type.
     */
    List<Vehicle> findByVehicleType(VehicleType vehicleType);

    /**
     * Checks if a license plate is already registered in the system.
     * Helps prevent duplicate entries during the addition or update of vehicle records.
     *
     * @param licensePlate The license plate string to verify.
     * @return True if the plate exists, false otherwise.
     */
    boolean existsByLicensePlate(String licensePlate);

    /**
     * Finds vehicles that are marked as available and have no conflicting bookings for a chosen duration.
     * Uses a subquery to exclude any vehicles that have overlapping reservations within the requested dates.
     *
     * @param start The desired start date of the rental.
     * @param end The desired end date of the rental.
     * @return A list of vehicles free for the specified time range.
     */
    @Query("SELECT v FROM Vehicle v WHERE v.status = 'AVAILABLE' AND v.id NOT IN (" +
            "SELECT b.vehicle.id FROM Booking b WHERE b.status = 'CONFIRMED' AND " +
            "(:start <= b.endDate AND :end >= b.startDate))")
    List<Vehicle> findAvailableVehiclesByDate(
            @Param("start") LocalDate start,
            @Param("end") LocalDate end
    );
}