package com.ashutosh.backend.service;

import com.ashutosh.backend.dto.request.VehicleRequestDTO;
import com.ashutosh.backend.dto.response.VehicleResponseDTO;
import com.ashutosh.backend.entity.Vehicle;
import com.ashutosh.backend.enums.VehicleFuelType;
import com.ashutosh.backend.enums.VehicleStatus;
import com.ashutosh.backend.enums.VehicleTransmission;
import com.ashutosh.backend.enums.VehicleType;
import com.ashutosh.backend.exception.ResourceNotFoundException;
import com.ashutosh.backend.repository.VehicleRepository;
import jakarta.persistence.EntityNotFoundException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

/**
 * Unit tests for the VehicleService class.
 * Perfectly mapped to the actual entity, enum, and repository structures.
 */
@ExtendWith(MockitoExtension.class)
class VehicleServiceTest {

    @Mock
    private VehicleRepository vehicleRepository;

    @InjectMocks
    private VehicleService vehicleService;

    private Vehicle mockVehicle;
    private VehicleRequestDTO vehicleRequest;

    @BeforeEach
    void setUp() {
        // Set up the standard mock entity matching your exact Enums
        mockVehicle = Vehicle.builder()
                .id(1L)
                .make("Mahindra")
                .model("Thar")
                .licensePlate("MH-12-AB-1234")
                .vehicleType(VehicleType.CAR)
                .vehicleFuelType(VehicleFuelType.DIESEL)
                .vehicleTransmission(VehicleTransmission.MANUAL)
                .seatingCapacity(4)
                .dailyRate(BigDecimal.valueOf(2500))
                .status(VehicleStatus.AVAILABLE)
                .build();

        // Set up the standard incoming request payload
        vehicleRequest = new VehicleRequestDTO();
        vehicleRequest.setMake("Mahindra");
        vehicleRequest.setModel("Thar");
        vehicleRequest.setLicensePlate("MH-12-AB-1234");
        vehicleRequest.setVehicleType(VehicleType.CAR);
        vehicleRequest.setVehicleFuelType(VehicleFuelType.DIESEL);
        vehicleRequest.setVehicleTransmission(VehicleTransmission.MANUAL);
        vehicleRequest.setSeatingCapacity(4);
        vehicleRequest.setDailyRate(BigDecimal.valueOf(2500));
    }

    // 1. ADD VEHICLE TESTS
    @Test
    void addVehicle_Success() {
        // GIVEN
        when(vehicleRepository.existsByLicensePlate(anyString())).thenReturn(false);
        when(vehicleRepository.save(any(Vehicle.class))).thenReturn(mockVehicle);

        // WHEN
        VehicleResponseDTO response = vehicleService.addVehicle(vehicleRequest);

        // THEN
        assertNotNull(response);
        assertEquals("Mahindra", response.getMake());
        assertEquals(VehicleStatus.AVAILABLE, response.getStatus());
        verify(vehicleRepository, times(1)).save(any(Vehicle.class));
    }

    @Test
    void addVehicle_DuplicateLicensePlate_ThrowsException() {
        // GIVEN
        when(vehicleRepository.existsByLicensePlate(anyString())).thenReturn(true);

        // WHEN & THEN
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class,
                () -> vehicleService.addVehicle(vehicleRequest));
        assertTrue(exception.getMessage().contains("already exists"));
        verify(vehicleRepository, never()).save(any(Vehicle.class));
    }

    @Test
    void addVehicle_InvalidDailyRate_ThrowsException() {
        // GIVEN
        when(vehicleRepository.existsByLicensePlate(anyString())).thenReturn(false);
        vehicleRequest.setDailyRate(BigDecimal.valueOf(-100)); // Negative rate

        // WHEN & THEN
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class,
                () -> vehicleService.addVehicle(vehicleRequest));
        assertTrue(exception.getMessage().contains("greater than 0"));
    }

    // 2. UPDATE VEHICLE TESTS
    @Test
    void updateVehicle_Success() {
        // GIVEN
        when(vehicleRepository.findById(1L)).thenReturn(Optional.of(mockVehicle));
        when(vehicleRepository.save(any(Vehicle.class))).thenReturn(mockVehicle);

        vehicleRequest.setDailyRate(BigDecimal.valueOf(3000));

        // WHEN
        VehicleResponseDTO response = vehicleService.updateVehicle(1L, vehicleRequest);

        // THEN
        assertNotNull(response);
        verify(vehicleRepository, times(1)).save(mockVehicle);
    }

    @Test
    void updateVehicle_NotFound_ThrowsEntityNotFoundException() {
        // GIVEN
        when(vehicleRepository.findById(99L)).thenReturn(Optional.empty());

        // WHEN & THEN
        assertThrows(EntityNotFoundException.class, () -> vehicleService.updateVehicle(99L, vehicleRequest));
    }

    // 3. DELETE (RETIRE) VEHICLE TESTS
    @Test
    void deleteVehicle_Success_SetsStatusToRetired() {
        // GIVEN
        when(vehicleRepository.findById(1L)).thenReturn(Optional.of(mockVehicle));

        // WHEN
        vehicleService.deleteVehicle(1L);

        // THEN (Note: The service code modifies the object but relies on Transactional to save it,
        // or we can just verify the object state changed in memory)
        assertEquals(VehicleStatus.RETIRED, mockVehicle.getStatus());
    }

    @Test
    void deleteVehicle_NotFound_ThrowsException() {
        // GIVEN
        when(vehicleRepository.findById(99L)).thenReturn(Optional.empty());

        // WHEN & THEN
        assertThrows(EntityNotFoundException.class, () -> vehicleService.deleteVehicle(99L));
    }

    // 4. RETRIEVAL & FILTERING TESTS
    @Test
    void getVehicleById_Success() {
        // GIVEN
        when(vehicleRepository.findById(1L)).thenReturn(Optional.of(mockVehicle));

        // WHEN
        VehicleResponseDTO response = vehicleService.getVehicleById(1L);

        // THEN
        assertNotNull(response);
        assertEquals(1L, response.getId());
    }

    @Test
    void getVehicleById_NotFound_ThrowsResourceNotFoundException() {
        // GIVEN
        when(vehicleRepository.findById(99L)).thenReturn(Optional.empty());

        // WHEN & THEN
        assertThrows(ResourceNotFoundException.class, () -> vehicleService.getVehicleById(99L));
    }

    @Test
    void getAllActiveVehicles_FiltersOutRetired() {
        // GIVEN: A list with one available and one retired vehicle
        Vehicle retiredVehicle = Vehicle.builder().id(2L).status(VehicleStatus.RETIRED).build();
        when(vehicleRepository.findAll()).thenReturn(List.of(mockVehicle, retiredVehicle));

        // WHEN
        List<VehicleResponseDTO> activeVehicles = vehicleService.getAllActiveVehicles();

        // THEN: Only the AVAILABLE vehicle should be returned
        assertEquals(1, activeVehicles.size());
        assertEquals(1L, activeVehicles.get(0).getId());
    }

    @Test
    void filterVehicles_ByDates_CallsCustomQuery() {
        // GIVEN
        LocalDate start = LocalDate.now();
        LocalDate end = LocalDate.now().plusDays(3);
        when(vehicleRepository.findAvailableVehiclesByDate(start, end)).thenReturn(List.of(mockVehicle));

        // WHEN
        List<VehicleResponseDTO> result = vehicleService.filterVehicles(null, null, start, end);

        // THEN
        assertEquals(1, result.size());
        verify(vehicleRepository, times(1)).findAvailableVehiclesByDate(start, end);
    }
}