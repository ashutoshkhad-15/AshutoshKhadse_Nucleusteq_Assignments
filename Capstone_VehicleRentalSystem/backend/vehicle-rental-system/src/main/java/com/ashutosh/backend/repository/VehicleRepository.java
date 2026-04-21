package com.ashutosh.backend.repository;

import com.ashutosh.backend.entity.Vehicle;
import com.ashutosh.backend.enums.VehicleStatus;
import com.ashutosh.backend.enums.VehicleType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface VehicleRepository extends JpaRepository<Vehicle, Long> {
    // these custom finders will allow the frontend to filter vehicles by their type (CAR/BIKE)
    // and only show ones that are currently 'AVAILABLE' to be booked.
    List<Vehicle> findByStatus(VehicleStatus status);
    List<Vehicle> findByVehicleTypeAndStatus(VehicleType type, VehicleStatus status);
    List<Vehicle> findByVehicleType(VehicleType vehicleType);
}