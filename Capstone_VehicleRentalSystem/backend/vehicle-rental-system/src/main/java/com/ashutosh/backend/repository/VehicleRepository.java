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

@Repository
public interface VehicleRepository extends JpaRepository<Vehicle, Long> {

    // Get all vehicles that are currently available to be booked
    List<Vehicle> findByStatus(VehicleStatus status);

    // Filter vehicles by both Type (CAR/BIKE) and Status (AVAILABLE)
    List<Vehicle> findByVehicleTypeAndStatus(VehicleType type, VehicleStatus status);

    // Filter vehicles by just Type
    List<Vehicle> findByVehicleType(VehicleType vehicleType);

    // Required by VehicleService.java to prevent duplicate license plates during POST/PUT
    boolean existsByLicensePlate(String licensePlate);

    @Query("SELECT v FROM Vehicle v WHERE v.status = 'AVAILABLE' AND v.id NOT IN (" +
            "SELECT b.vehicle.id FROM Booking b WHERE b.status = 'CONFIRMED' AND " +
            "(:start <= b.endDate AND :end >= b.startDate))")
    List<Vehicle> findAvailableVehiclesByDate(
            @Param("start") LocalDate start,
            @Param("end") LocalDate end
    );
}