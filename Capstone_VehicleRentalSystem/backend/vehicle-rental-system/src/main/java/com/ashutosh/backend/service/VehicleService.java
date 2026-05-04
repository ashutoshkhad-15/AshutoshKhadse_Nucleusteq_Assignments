package com.ashutosh.backend.service;

import com.ashutosh.backend.dto.request.VehicleRequestDTO;
import com.ashutosh.backend.dto.response.VehicleResponseDTO;
import com.ashutosh.backend.entity.Vehicle;
import com.ashutosh.backend.enums.VehicleStatus;
import com.ashutosh.backend.enums.VehicleType;
import com.ashutosh.backend.exception.ResourceNotFoundException;
import com.ashutosh.backend.repository.VehicleRepository;
import jakarta.persistence.EntityNotFoundException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.List;

/**
 * Service class responsible for managing vehicle inventory.
 * Handles the business logic for adding, updating, and filtering vehicles.
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class VehicleService {

    private final VehicleRepository vehicleRepository;

    /**
     * Validates and persists new vehicle details to the database.
     * Ensures that the license plate is unique and the daily rate is valid before saving.
     *
     * @param request The vehicle data transfer object containing creation details.
     * @return VehicleResponseDTO The successfully saved vehicle data.
     */
    @Transactional
    public VehicleResponseDTO addVehicle(VehicleRequestDTO request) {
        String licensePlate = request.getLicensePlate().trim().toUpperCase();
        log.info("Attempting to add a new vehicle with license plate: {}", licensePlate);

        if (vehicleRepository.existsByLicensePlate(licensePlate)) {
            log.warn("Vehicle addition failed: License plate {} already exists in the system.", licensePlate);
            throw new IllegalArgumentException("A vehicle with this license plate already exists.");
        }

        if (request.getDailyRate().doubleValue() <= 0) {
            log.warn("Vehicle addition failed: Invalid daily rate provided ({}).", request.getDailyRate());
            throw new IllegalArgumentException("Daily rate must be greater than 0.");
        }
        if (request.getSeatingCapacity() <= 0) {
            log.warn("Vehicle addition failed: Invalid seating capacity provided ({}).", request.getSeatingCapacity());
            throw new IllegalArgumentException("Seating capacity must be valid.");
        }

        // Map the validated request data to the Vehicle entity
        Vehicle vehicle = Vehicle.builder()
                .make(request.getMake().trim())
                .model(request.getModel().trim())
                .licensePlate(licensePlate)
                .vehicleType(request.getVehicleType())
                .vehicleFuelType(request.getVehicleFuelType())
                .vehicleTransmission(request.getVehicleTransmission())
                .seatingCapacity(request.getSeatingCapacity())
                .dailyRate(request.getDailyRate())
                .status(VehicleStatus.AVAILABLE) // New vehicles default to AVAILABLE status
                .imageUrl(request.getImageUrl())
                .build();

        Vehicle savedVehicle = vehicleRepository.save(vehicle);
        log.info("Successfully added new vehicle: {} {} with ID: {}", savedVehicle.getMake(), savedVehicle.getModel(), savedVehicle.getId());

        return mapToResponseDTO(savedVehicle);
    }

    /**
     * Updates an existing vehicle's records.
     * Includes a check to ensure the new license plate does not conflict with another existing vehicle.
     *
     * @param id The unique identifier of the vehicle being edited.
     * @param request The updated vehicle details.
     * @return VehicleResponseDTO The updated vehicle.
     */
    @Transactional
    public VehicleResponseDTO updateVehicle(Long id, VehicleRequestDTO request) {
        log.info("Attempting to update vehicle with ID: {}", id);

        Vehicle vehicle = vehicleRepository.findById(id)
                .orElseThrow(() -> {
                    log.error("Vehicle update failed: Vehicle not found with ID: {}", id);
                    return new EntityNotFoundException("Vehicle not found with ID: " + id);
                });

        String newPlate = request.getLicensePlate().trim().toUpperCase();

        if (!vehicle.getLicensePlate().equals(newPlate) && vehicleRepository.existsByLicensePlate(newPlate)) {
            log.warn("Vehicle update failed for ID {}: License plate {} is registered to another vehicle.", id, newPlate);
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

        Vehicle updatedVehicle = vehicleRepository.save(vehicle);
        log.info("Successfully updated vehicle with ID: {}", updatedVehicle.getId());

        return mapToResponseDTO(updatedVehicle);
    }

    /**
     * Performs a soft delete by marking the vehicle's status as RETIRED.
     * This preserves historical booking records instead of permanently deleting the entity.
     *
     * @param id The unique identifier of the vehicle to remove.
     */
    @Transactional
    public void deleteVehicle(Long id) {
        log.info("Attempting to soft delete (RETIRE) vehicle with ID: {}", id);

        Vehicle vehicle = vehicleRepository.findById(id)
                .orElseThrow(() -> {
                    log.error("Vehicle deletion failed: Vehicle not found with ID: {}", id);
                    return new EntityNotFoundException("Vehicle not found with ID: " + id);
                });

        vehicle.setStatus(VehicleStatus.RETIRED);
        log.info("Successfully marked vehicle ID: {} as RETIRED", id);
    }

    /**
     * Retrieves a comprehensive list of all vehicles, including retired ones.
     * Primarily intended for the administrative dashboard view.
     *
     * @return List of all vehicles.
     */
    @Transactional(readOnly = true)
    public List<VehicleResponseDTO> getAllVehicles() {
        log.info("Fetching complete inventory of all vehicles.");
        return vehicleRepository.findAll()
                .stream()
                .map(this::mapToResponseDTO)
                .toList();
    }

    /**
     * Dynamically filters vehicles based on frontend parameters.
     * If no specific filters are passed, it defaults to returning the full inventory.
     *
     * @param type The vehicle type (e.g., CAR, BIKE).
     * @param status The current operational status.
     * @param startDate The requested rental start date.
     * @param endDate The requested rental end date.
     * @return List of matching vehicles.
     */
    @Transactional(readOnly = true)
    public List<VehicleResponseDTO> filterVehicles(VehicleType type, VehicleStatus status, LocalDate startDate, LocalDate endDate) {
        log.info("Filtering vehicles. Parameters - Type: {}, Status: {}, StartDate: {}, EndDate: {}", type, status, startDate, endDate);
        List<Vehicle> vehicles = fetchVehiclesForFilter(type, status, startDate, endDate);

        return vehicles.stream()
                .filter(v -> v.getStatus() != VehicleStatus.RETIRED)
                .filter(v -> type == null || v.getVehicleType().equals(type))
                .filter(v -> status == null || v.getStatus().equals(status))
                .map(this::mapToResponseDTO)
                .toList();
    }

    /**
     * Applies the same fleet filtering semantics for administrators, while preserving
     * visibility into RETIRED units that should remain hidden from the public catalog.
     *
     * @param type The vehicle type (e.g., CAR, BIKE).
     * @param status The current operational status.
     * @param startDate The requested rental start date.
     * @param endDate The requested rental end date.
     * @return List of matching vehicles, including retired ones when requested.
     */
    @Transactional(readOnly = true)
    public List<VehicleResponseDTO> filterVehiclesForAdmin(VehicleType type, VehicleStatus status, LocalDate startDate, LocalDate endDate) {
        log.info("Admin fleet filter. Parameters - Type: {}, Status: {}, StartDate: {}, EndDate: {}", type, status, startDate, endDate);
        List<Vehicle> vehicles = fetchVehiclesForFilter(type, status, startDate, endDate);

        return vehicles.stream()
                .filter(v -> type == null || v.getVehicleType().equals(type))
                .filter(v -> status == null || v.getStatus().equals(status))
                .map(this::mapToResponseDTO)
                .toList();
    }

    /**
     * Retrieves specific details for a single vehicle.
     * Typically used when viewing vehicle details on the user interface.
     *
     * @param id The unique identifier of the vehicle.
     * @return The corresponding vehicle details.
     */
    @Transactional(readOnly = true)
    public VehicleResponseDTO getVehicleById(Long id) {
        log.info("Fetching details for vehicle ID: {}", id);
        Vehicle vehicle = vehicleRepository.findById(id)
                .orElseThrow(() -> {
                    log.error("Vehicle fetch failed: Vehicle not found with ID: {}", id);
                    return new ResourceNotFoundException("Vehicle not found with ID: " + id);
                });
        return mapToResponseDTO(vehicle);
    }

    /**
     * Retrieves all operational vehicles for the public catalog.
     * Explicitly filters out RETIRED units to prevent invalid bookings.
     *
     * @return List of active vehicles.
     */
    @Transactional(readOnly = true)
    public List<VehicleResponseDTO> getAllActiveVehicles() {
        log.info("Fetching all active vehicles for public catalog.");

        return vehicleRepository.findAll().stream()
                .filter(v -> v.getStatus() != VehicleStatus.RETIRED)
                .map(this::mapToResponseDTO)
                .toList();
    }

    /**
     * Converts the Vehicle database entity into a Data Transfer Object (DTO).
     * Ensures internal database models are not exposed directly to the frontend.
     *
     * @param vehicle The database entity.
     * @return The formatted response DTO.
     */
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

    private List<Vehicle> fetchVehiclesForFilter(VehicleType type, VehicleStatus status, LocalDate startDate, LocalDate endDate) {
        if (startDate != null && endDate != null && (status == null || status == VehicleStatus.AVAILABLE)) {
            return vehicleRepository.findAvailableVehiclesByDate(startDate, endDate);
        }
        if (type != null && status != null) {
            return vehicleRepository.findByVehicleTypeAndStatus(type, status);
        }
        if (type != null) {
            return vehicleRepository.findByVehicleType(type);
        }
        if (status != null) {
            return vehicleRepository.findByStatus(status);
        }
        return vehicleRepository.findAll();
    }
}
