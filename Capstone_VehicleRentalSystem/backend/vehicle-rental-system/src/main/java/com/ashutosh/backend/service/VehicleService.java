package com.ashutosh.backend.service;

import com.ashutosh.backend.dto.request.VehicleRequestDTO;
import com.ashutosh.backend.dto.response.VehicleResponseDTO;
import com.ashutosh.backend.entity.Vehicle;
import com.ashutosh.backend.enums.VehicleStatus;
import com.ashutosh.backend.enums.VehicleType;
import com.ashutosh.backend.enums.VehicleFuelType;
import com.ashutosh.backend.enums.VehicleTransmission;
import com.ashutosh.backend.exception.ResourceNotFoundException;
import com.ashutosh.backend.repository.VehicleRepository;
import jakarta.persistence.EntityNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class VehicleService {

    private final VehicleRepository vehicleRepository;

    // 1. ADD VEHICLE (ADMIN)
    @Transactional
    public VehicleResponseDTO addVehicle(VehicleRequestDTO request) {
        String licensePlate = request.getLicensePlate().trim().toUpperCase();

        if (vehicleRepository.existsByLicensePlate(licensePlate)) {
            throw new IllegalArgumentException("A vehicle with this license plate already exists.");
        }

        if (request.getDailyRate().doubleValue() <= 0) {
            throw new IllegalArgumentException("Daily rate must be greater than 0.");
        }
        if (request.getSeatingCapacity() <= 0) {
            throw new IllegalArgumentException("Seating capacity must be valid.");
        }

        // Convert the validated DTO into our strict Entity using the Builder pattern
        Vehicle vehicle = Vehicle.builder()
                .make(request.getMake().trim())
                .model(request.getModel().trim())
                .licensePlate(licensePlate)
                .vehicleType(request.getVehicleType())
                .vehicleFuelType(request.getVehicleFuelType())
                .vehicleTransmission(request.getVehicleTransmission())
                .seatingCapacity(request.getSeatingCapacity())
                .dailyRate(request.getDailyRate())
                .status(VehicleStatus.AVAILABLE) // Brand new vehicles are always available
                .imageUrl(request.getImageUrl())
                .build();

        Vehicle savedVehicle = vehicleRepository.save(vehicle);
        return mapToResponseDTO(savedVehicle);
    }

    // 2. UPDATE VEHICLE (ADMIN)
    @Transactional
    public VehicleResponseDTO updateVehicle(Long id, VehicleRequestDTO request) {
        Vehicle vehicle = vehicleRepository.findById(id)
                .orElseThrow(() -> new EntityNotFoundException("Vehicle not found with ID: " + id));

        String newPlate = request.getLicensePlate().trim().toUpperCase();
        // Guard Rail: Ensure the admin isn't changing the plate to one that already exists on ANOTHER car
        if (!vehicle.getLicensePlate().equals(newPlate) &&
                vehicleRepository.existsByLicensePlate(newPlate)) {
            throw new IllegalArgumentException("License plate is already registered to another vehicle.");
        }

        vehicle.setMake(request.getMake());
        vehicle.setModel(request.getModel());
        vehicle.setLicensePlate(newPlate);
        vehicle.setVehicleType(request.getVehicleType());
        vehicle.setVehicleFuelType(request.getVehicleFuelType());
        vehicle.setVehicleTransmission(request.getVehicleTransmission());
        vehicle.setSeatingCapacity(request.getSeatingCapacity());
        vehicle.setDailyRate(request.getDailyRate());
        vehicle.setImageUrl(request.getImageUrl());

        if (request.getStatus() != null) {
            vehicle.setStatus(request.getStatus());
        }

        // Save and return
        Vehicle updatedVehicle = vehicleRepository.save(vehicle);
        return mapToResponseDTO(updatedVehicle);
    }

    // 3. DELETE VEHICLE (ADMIN - Soft Delete)
    @Transactional
    public void deleteVehicle(Long id) {
        Vehicle vehicle = vehicleRepository.findById(id)
                .orElseThrow(() -> new EntityNotFoundException("Vehicle not found with ID: " + id));
        vehicle.setStatus(VehicleStatus.RETIRED);
    }

    // 4. GET ALL VEHICLES
    @Transactional(readOnly = true)
    public List<VehicleResponseDTO> getAllVehicles() {
        return vehicleRepository.findAll()
                .stream()
                .map(this::mapToResponseDTO)
                .toList();
    }

    // 5. FILTER VEHICLES (By Type & Availability)
    @Transactional(readOnly = true)
    public List<VehicleResponseDTO> filterVehicles(VehicleType type, VehicleStatus status, LocalDate startDate, LocalDate endDate) {
        List<Vehicle> vehicles;

        if (startDate != null && endDate != null) {
            vehicles = vehicleRepository.findAvailableVehiclesByDate(startDate, endDate);
        } else if (type != null && status != null) {
            vehicles = vehicleRepository.findByVehicleTypeAndStatus(type, status);
        } else if (type != null) {
            vehicles = vehicleRepository.findByVehicleType(type);
        } else if (status != null) {
            vehicles = vehicleRepository.findByStatus(status);
        } else {
            // Fallback if no filters are provided
            vehicles = vehicleRepository.findAll();
        }

        return vehicles.stream()
                .filter(v -> v.getStatus() != VehicleStatus.RETIRED)
                .filter(v -> type == null || v.getVehicleType().equals(type))
                .filter(v -> status == null || v.getStatus().equals(status))
                .map(this::mapToResponseDTO)
                .toList();
    }
    // Get Single Vehicle by ID
    @Transactional(readOnly = true)
    public VehicleResponseDTO getVehicleById(Long id) {
        Vehicle vehicle = vehicleRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Vehicle not found with ID: " + id));
        return mapToResponseDTO(vehicle);
    }

    @Transactional(readOnly = true)
    public List<VehicleResponseDTO> getAllActiveVehicles() {
        // Exclude RETIRED vehicles from the public view
        return vehicleRepository.findAll().stream()
                .filter(v -> v.getStatus() != VehicleStatus.RETIRED)
                .map(this::mapToResponseDTO)
                .toList();
    }

    // HELPER METHOD: Entity to DTO Mapper
    private VehicleResponseDTO mapToResponseDTO(Vehicle vehicle) {
        return VehicleResponseDTO.builder()
                .id(vehicle.getId())
                .make(vehicle.getMake())
                .model(vehicle.getModel())
                .licensePlate(vehicle.getLicensePlate())
                .vehicleType(vehicle.getVehicleType())
                .vehicleFuelType(vehicle.getVehicleFuelType())
                .vehicleTransmission(vehicle.getVehicleTransmission())
                .seatingCapacity(vehicle.getSeatingCapacity())
                .dailyRate(vehicle.getDailyRate())
                .status(vehicle.getStatus())
                .imageUrl(vehicle.getImageUrl())
                .build();
    }
}