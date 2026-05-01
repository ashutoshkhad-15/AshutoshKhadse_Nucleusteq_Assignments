package com.ashutosh.backend.controller;

import com.ashutosh.backend.dto.request.VehicleRequestDTO;
import com.ashutosh.backend.dto.response.VehicleResponseDTO;
import com.ashutosh.backend.enums.VehicleStatus;
import com.ashutosh.backend.enums.VehicleType;
import com.ashutosh.backend.service.VehicleService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;

/**
 * REST controller responsible for managing the vehicle inventory.
 * Provides endpoints for administrative CRUD operations and public catalog filtering.
 */
@RestController
@RequestMapping("/api/vehicles")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
@Slf4j
public class VehicleController {

    private final VehicleService vehicleService;

    /**
     * Processes an administrative request to add a new vehicle to the fleet.
     *
     * @param request The vehicle details provided by the admin.
     * @return ResponseEntity containing the saved vehicle details and a 201 Created status.
     */
    @PostMapping
    public ResponseEntity<VehicleResponseDTO> addVehicle(@Valid @RequestBody VehicleRequestDTO request) {
        log.info("REST request received: Add new vehicle with license plate: {}", request.getLicensePlate());

        VehicleResponseDTO response = vehicleService.addVehicle(request);

        log.info("Successfully processed vehicle addition. Returned vehicle ID: {}", response.getId());
        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }

    /**
     * Processes an administrative request to update an existing vehicle's information.
     *
     * @param id The unique identifier of the vehicle to update.
     * @param request The updated vehicle details.
     * @return ResponseEntity containing the updated vehicle data.
     */
    @PutMapping("/{id}")
    public ResponseEntity<VehicleResponseDTO> updateVehicle(
            @PathVariable Long id,
            @Valid @RequestBody VehicleRequestDTO request) {
        log.info("REST request received: Update vehicle ID: {}", id);

        VehicleResponseDTO response = vehicleService.updateVehicle(id, request);
        return ResponseEntity.ok(response);
    }

    /**
     * Processes an administrative request to safely remove a vehicle from circulation.
     * Triggers a soft delete (status change) rather than a hard database deletion to preserve history.
     *
     * @param id The unique identifier of the vehicle to retire.
     * @return ResponseEntity with a 204 No Content status upon success.
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteVehicle(@PathVariable Long id) {
        log.info("REST request received: Soft delete (RETIRE) vehicle ID: {}", id);

        vehicleService.deleteVehicle(id);
        return ResponseEntity.noContent().build();
    }

    /**
     * Retrieves all currently active and available vehicles for the public-facing catalog.
     * Excludes any vehicles marked as retired.
     *
     * @return ResponseEntity containing a list of active vehicles.
     */
    @GetMapping
    public ResponseEntity<List<VehicleResponseDTO>> getActiveVehicles() {
        log.info("REST request received: Fetch all active vehicles for public catalog.");

        return ResponseEntity.ok(vehicleService.getAllActiveVehicles());
    }

    /**
     * Retrieves the complete vehicle inventory, including retired units.
     * Intended strictly for administrative dashboard oversight.
     *
     * @return ResponseEntity containing all vehicles in the database.
     */
    @GetMapping("/admin/all")
    public ResponseEntity<List<VehicleResponseDTO>> getAllVehicles() {
        log.info("REST request received: Fetch complete vehicle inventory (Admin Access).");

        return ResponseEntity.ok(vehicleService.getAllVehicles());
    }

    /**
     * Retrieves the specific details of a single vehicle by its ID.
     * Used primarily for rendering the individual vehicle details page on the frontend.
     *
     * @param id The unique identifier of the vehicle.
     * @return ResponseEntity containing the vehicle's details.
     */
    @GetMapping("/{id}")
    public ResponseEntity<VehicleResponseDTO> getVehicleById(@PathVariable Long id) {
        log.info("REST request received: Fetch details for vehicle ID: {}", id);

        return ResponseEntity.ok(vehicleService.getVehicleById(id));
    }

    /**
     * Dynamically filters the vehicle catalog based on user-selected criteria.
     * Supports filtering by type, current status, and date availability.
     *
     * @param type Optional filter for vehicle category (e.g., CAR, BIKE).
     * @param status Optional filter for current operational status.
     * @param startDate Optional filter for rental start date.
     * @param endDate Optional filter for rental end date.
     * @return ResponseEntity containing the list of matching vehicles.
     */
    @GetMapping("/filter")
    public ResponseEntity<List<VehicleResponseDTO>> filterVehicles(
            @RequestParam(required = false) VehicleType type,
            @RequestParam(required = false) VehicleStatus status,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate startDate,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate endDate) {

        log.info("REST request received: Filter vehicles. Parameters - Type: {}, Status: {}, Start: {}, End: {}",
                type, status, startDate, endDate);

        return ResponseEntity.ok(vehicleService.filterVehicles(type, status, startDate, endDate));
    }

    /**
     * Applies fleet filters for administrative inventory views.
     * Unlike the public catalog filter, this endpoint preserves RETIRED vehicles
     * so admins can audit the full fleet lifecycle.
     *
     * @param type Optional filter for vehicle category (e.g., CAR, BIKE).
     * @param status Optional filter for current operational status.
     * @param startDate Optional filter for rental start date.
     * @param endDate Optional filter for rental end date.
     * @return ResponseEntity containing the list of matching vehicles.
     */
    @GetMapping("/admin/filter")
    public ResponseEntity<List<VehicleResponseDTO>> filterVehiclesForAdmin(
            @RequestParam(required = false) VehicleType type,
            @RequestParam(required = false) VehicleStatus status,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate startDate,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate endDate) {

        log.info("REST request received: Admin filter vehicles. Parameters - Type: {}, Status: {}, Start: {}, End: {}",
                type, status, startDate, endDate);

        return ResponseEntity.ok(vehicleService.filterVehiclesForAdmin(type, status, startDate, endDate));
    }
}
