package com.ashutosh.backend.controller;

import com.ashutosh.backend.dto.request.VehicleRequestDTO;
import com.ashutosh.backend.dto.response.VehicleResponseDTO;
import com.ashutosh.backend.enums.VehicleStatus;
import com.ashutosh.backend.enums.VehicleType;
import com.ashutosh.backend.service.VehicleService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/vehicles")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
public class VehicleController {

    private final VehicleService vehicleService;

    // 1. ADD VEHICLE
    @PostMapping
    public ResponseEntity<VehicleResponseDTO> addVehicle(@Valid @RequestBody VehicleRequestDTO request) {
        VehicleResponseDTO response = vehicleService.addVehicle(request);
        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }

    // 2. UPDATE VEHICLE
    @PutMapping("/{id}")
    public ResponseEntity<VehicleResponseDTO> updateVehicle(
            @PathVariable Long id,
            @Valid @RequestBody VehicleRequestDTO request) {
        VehicleResponseDTO response = vehicleService.updateVehicle(id, request);
        return ResponseEntity.ok(response);
    }

    // 3. DELETE VEHICLE
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteVehicle(@PathVariable Long id) {
        vehicleService.deleteVehicle(id);
        return ResponseEntity.noContent().build();
    }

    // 4. GET ALL VEHICLES
    @GetMapping
    public ResponseEntity<List<VehicleResponseDTO>> getAllVehicles() {
        return ResponseEntity.ok(vehicleService.getAllVehicles());
    }

    // 5. FILTER VEHICLES
    @GetMapping("/filter")
    public ResponseEntity<List<VehicleResponseDTO>> filterVehicles(
            @RequestParam(required = false) VehicleType type,
            @RequestParam(required = false) VehicleStatus status) {
        return ResponseEntity.ok(vehicleService.filterVehicles(type, status));
    }
}