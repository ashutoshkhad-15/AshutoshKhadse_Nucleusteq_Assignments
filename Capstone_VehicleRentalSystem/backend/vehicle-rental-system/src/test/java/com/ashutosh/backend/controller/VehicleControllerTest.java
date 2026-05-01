package com.ashutosh.backend.controller;

import com.ashutosh.backend.dto.request.VehicleRequestDTO;
import com.ashutosh.backend.dto.response.VehicleResponseDTO;
import com.ashutosh.backend.enums.VehicleFuelType;
import com.ashutosh.backend.enums.VehicleStatus;
import com.ashutosh.backend.enums.VehicleTransmission;
import com.ashutosh.backend.enums.VehicleType;
import com.ashutosh.backend.exception.GlobalExceptionHandler;
import com.ashutosh.backend.exception.ResourceNotFoundException;
import com.ashutosh.backend.service.VehicleService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.validation.beanvalidation.LocalValidatorFactoryBean;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoMoreInteractions;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@ExtendWith(MockitoExtension.class)
class VehicleControllerTest {

    @Mock
    private VehicleService vehicleService;

    @InjectMocks
    private VehicleController vehicleController;

    private MockMvc mockMvc;
    private ObjectMapper objectMapper;
    private VehicleRequestDTO vehicleRequest;
    private VehicleResponseDTO vehicleResponse;
    private VehicleResponseDTO updatedVehicleResponse;

    @BeforeEach
    void setUp() {
        LocalValidatorFactoryBean validator = new LocalValidatorFactoryBean();
        validator.afterPropertiesSet();

        mockMvc = MockMvcBuilders.standaloneSetup(vehicleController)
                .setControllerAdvice(new GlobalExceptionHandler())
                .setValidator(validator)
                .build();

        objectMapper = new ObjectMapper().findAndRegisterModules();

        vehicleRequest = new VehicleRequestDTO();
        vehicleRequest.setMake("Toyota");
        vehicleRequest.setModel("Camry");
        vehicleRequest.setLicensePlate("MH-12-AB-1234");
        vehicleRequest.setVehicleType(VehicleType.CAR);
        vehicleRequest.setVehicleFuelType(VehicleFuelType.PETROL);
        vehicleRequest.setVehicleTransmission(VehicleTransmission.AUTOMATIC);
        vehicleRequest.setSeatingCapacity(5);
        vehicleRequest.setDailyRate(BigDecimal.valueOf(2500));
        vehicleRequest.setImageUrl("https://example.com/camry.jpg");

        vehicleResponse = buildVehicleResponse(1L, VehicleStatus.AVAILABLE, BigDecimal.valueOf(2500));
        updatedVehicleResponse = buildVehicleResponse(1L, VehicleStatus.MAINTENANCE, BigDecimal.valueOf(3000));
    }

    @Test
    void addVehicle_ReturnsCreatedVehicle() throws Exception {
        // GIVEN
        when(vehicleService.addVehicle(any(VehicleRequestDTO.class))).thenReturn(vehicleResponse);

        // WHEN
        mockMvc.perform(post("/api/vehicles")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(vehicleRequest)))

                // THEN
                .andExpect(status().isCreated())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$.id").value(1L))
                .andExpect(jsonPath("$.make").value("Toyota"))
                .andExpect(jsonPath("$.model").value("Camry"))
                .andExpect(jsonPath("$.licensePlate").value("MH-12-AB-1234"))
                .andExpect(jsonPath("$.vehicleType").value("CAR"))
                .andExpect(jsonPath("$.vehicleFuelType").value("PETROL"))
                .andExpect(jsonPath("$.vehicleTransmission").value("AUTOMATIC"))
                .andExpect(jsonPath("$.seatingCapacity").value(5))
                .andExpect(jsonPath("$.dailyRate").value(2500))
                .andExpect(jsonPath("$.status").value("AVAILABLE"))
                .andExpect(jsonPath("$.imageUrl").value("https://example.com/camry.jpg"));

        ArgumentCaptor<VehicleRequestDTO> captor = ArgumentCaptor.forClass(VehicleRequestDTO.class);
        verify(vehicleService, times(1)).addVehicle(captor.capture());
        VehicleRequestDTO capturedRequest = captor.getValue();
        assertNotNull(capturedRequest);
        assertEquals("Toyota", capturedRequest.getMake());
        assertEquals("Camry", capturedRequest.getModel());
        assertEquals("MH-12-AB-1234", capturedRequest.getLicensePlate());
        verifyNoMoreInteractions(vehicleService);
    }

    @Test
    void addVehicle_WhenRequestIsInvalid_ReturnsBadRequest() throws Exception {
        // GIVEN
        VehicleRequestDTO invalidRequest = new VehicleRequestDTO();
        invalidRequest.setLicensePlate("invalid plate");
        invalidRequest.setSeatingCapacity(0);
        invalidRequest.setDailyRate(BigDecimal.valueOf(-100));

        // WHEN
        mockMvc.perform(post("/api/vehicles")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(invalidRequest)))

                // THEN
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.status").value(400))
                .andExpect(jsonPath("$.errors.make").value("Make cannot be blank"))
                .andExpect(jsonPath("$.errors.model").value("Model cannot be blank"))
                .andExpect(jsonPath("$.errors.licensePlate")
                        .value("License plate must contain only uppercase letters and numbers and hyphens"))
                .andExpect(jsonPath("$.errors.vehicleType").value("Vehicle type is required"))
                .andExpect(jsonPath("$.errors.vehicleFuelType").value("Fuel type is required"))
                .andExpect(jsonPath("$.errors.vehicleTransmission").value("Transmission is required"))
                .andExpect(jsonPath("$.errors.seatingCapacity").value("Seating capacity must be at least 1"))
                .andExpect(jsonPath("$.errors.dailyRate").value("Daily rate must be strictly greater than zero"));

        verify(vehicleService, never()).addVehicle(any(VehicleRequestDTO.class));
    }

    @Test
    void addVehicle_WhenServiceThrowsIllegalArgumentException_ReturnsBadRequest() throws Exception {
        // GIVEN
        when(vehicleService.addVehicle(any(VehicleRequestDTO.class)))
                .thenThrow(new IllegalArgumentException("A vehicle with this license plate already exists."));

        // WHEN
        mockMvc.perform(post("/api/vehicles")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(vehicleRequest)))

                // THEN
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.status").value(400))
                .andExpect(jsonPath("$.error").value("A vehicle with this license plate already exists."));

        verify(vehicleService, times(1)).addVehicle(any(VehicleRequestDTO.class));
    }

    @Test
    void updateVehicle_ReturnsUpdatedVehicle() throws Exception {
        // GIVEN
        vehicleRequest.setDailyRate(BigDecimal.valueOf(3000));
        vehicleRequest.setStatus(VehicleStatus.MAINTENANCE);
        when(vehicleService.updateVehicle(any(Long.class), any(VehicleRequestDTO.class))).thenReturn(updatedVehicleResponse);

        // WHEN
        mockMvc.perform(put("/api/vehicles/1")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(vehicleRequest)))

                // THEN
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1L))
                .andExpect(jsonPath("$.dailyRate").value(3000))
                .andExpect(jsonPath("$.status").value("MAINTENANCE"));

        ArgumentCaptor<Long> idCaptor = ArgumentCaptor.forClass(Long.class);
        ArgumentCaptor<VehicleRequestDTO> requestCaptor = ArgumentCaptor.forClass(VehicleRequestDTO.class);
        verify(vehicleService, times(1)).updateVehicle(idCaptor.capture(), requestCaptor.capture());
        assertEquals(1L, idCaptor.getValue());
        assertEquals(BigDecimal.valueOf(3000), requestCaptor.getValue().getDailyRate());
        assertEquals(VehicleStatus.MAINTENANCE, requestCaptor.getValue().getStatus());
    }

    @Test
    void deleteVehicle_ReturnsNoContent() throws Exception {
        // GIVEN

        // WHEN
        mockMvc.perform(delete("/api/vehicles/1"))

                // THEN
                .andExpect(status().isNoContent());

        verify(vehicleService, times(1)).deleteVehicle(1L);
    }

    @Test
    void getActiveVehicles_ReturnsActiveVehicleList() throws Exception {
        // GIVEN
        VehicleResponseDTO bikeResponse = VehicleResponseDTO.builder()
                .id(2L)
                .make("Yamaha")
                .model("FZ")
                .licensePlate("MH-14-CD-5678")
                .vehicleType(VehicleType.BIKE)
                .vehicleFuelType(VehicleFuelType.PETROL)
                .vehicleTransmission(VehicleTransmission.MANUAL)
                .seatingCapacity(2)
                .dailyRate(BigDecimal.valueOf(1200))
                .status(VehicleStatus.AVAILABLE)
                .imageUrl("https://example.com/fz.jpg")
                .build();
        when(vehicleService.getAllActiveVehicles()).thenReturn(List.of(vehicleResponse, bikeResponse));

        // WHEN
        mockMvc.perform(get("/api/vehicles"))

                // THEN
                .andExpect(status().isOk())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$[0].id").value(1L))
                .andExpect(jsonPath("$[0].vehicleType").value("CAR"))
                .andExpect(jsonPath("$[1].id").value(2L))
                .andExpect(jsonPath("$[1].vehicleType").value("BIKE"));

        verify(vehicleService, times(1)).getAllActiveVehicles();
    }

    @Test
    void getAllVehicles_ReturnsInventory() throws Exception {
        // GIVEN
        VehicleResponseDTO retiredVehicle = buildVehicleResponse(3L, VehicleStatus.RETIRED, BigDecimal.valueOf(2000));
        when(vehicleService.getAllVehicles()).thenReturn(List.of(vehicleResponse, retiredVehicle));

        // WHEN
        mockMvc.perform(get("/api/vehicles/admin/all"))

                // THEN
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].id").value(1L))
                .andExpect(jsonPath("$[1].id").value(3L))
                .andExpect(jsonPath("$[1].status").value("RETIRED"));

        verify(vehicleService, times(1)).getAllVehicles();
    }

    @Test
    void getVehicleById_ReturnsVehicle() throws Exception {
        // GIVEN
        when(vehicleService.getVehicleById(1L)).thenReturn(vehicleResponse);

        // WHEN
        mockMvc.perform(get("/api/vehicles/1"))

                // THEN
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1L))
                .andExpect(jsonPath("$.make").value("Toyota"))
                .andExpect(jsonPath("$.status").value("AVAILABLE"));

        verify(vehicleService, times(1)).getVehicleById(1L);
    }

    @Test
    void getVehicleById_WhenNotFound_ReturnsNotFound() throws Exception {
        // GIVEN
        when(vehicleService.getVehicleById(99L)).thenThrow(new ResourceNotFoundException("Vehicle not found with ID: 99"));

        // WHEN
        mockMvc.perform(get("/api/vehicles/99"))

                // THEN
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.status").value(404))
                .andExpect(jsonPath("$.error").value("Vehicle not found with ID: 99"));

        verify(vehicleService, times(1)).getVehicleById(99L);
    }

    @Test
    void filterVehicles_WithAllQueryParameters_DelegatesAndReturnsFilteredResults() throws Exception {
        // GIVEN
        LocalDate startDate = LocalDate.of(2026, 5, 10);
        LocalDate endDate = LocalDate.of(2026, 5, 12);
        when(vehicleService.filterVehicles(any(VehicleType.class), any(VehicleStatus.class), any(LocalDate.class), any(LocalDate.class)))
                .thenReturn(List.of(vehicleResponse));

        // WHEN
        mockMvc.perform(get("/api/vehicles/filter")
                        .param("type", "CAR")
                        .param("status", "AVAILABLE")
                        .param("startDate", "2026-05-10")
                        .param("endDate", "2026-05-12"))

                // THEN
                .andExpect(status().isOk())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$[0].id").value(1L))
                .andExpect(jsonPath("$[0].licensePlate").value("MH-12-AB-1234"));

        ArgumentCaptor<VehicleType> typeCaptor = ArgumentCaptor.forClass(VehicleType.class);
        ArgumentCaptor<VehicleStatus> statusCaptor = ArgumentCaptor.forClass(VehicleStatus.class);
        ArgumentCaptor<LocalDate> startDateCaptor = ArgumentCaptor.forClass(LocalDate.class);
        ArgumentCaptor<LocalDate> endDateCaptor = ArgumentCaptor.forClass(LocalDate.class);
        verify(vehicleService, times(1)).filterVehicles(
                typeCaptor.capture(),
                statusCaptor.capture(),
                startDateCaptor.capture(),
                endDateCaptor.capture()
        );
        assertEquals(VehicleType.CAR, typeCaptor.getValue());
        assertEquals(VehicleStatus.AVAILABLE, statusCaptor.getValue());
        assertEquals(startDate, startDateCaptor.getValue());
        assertEquals(endDate, endDateCaptor.getValue());
    }

    private VehicleResponseDTO buildVehicleResponse(Long id, VehicleStatus status, BigDecimal dailyRate) {
        return VehicleResponseDTO.builder()
                .id(id)
                .make("Toyota")
                .model("Camry")
                .licensePlate("MH-12-AB-1234")
                .vehicleType(VehicleType.CAR)
                .vehicleFuelType(VehicleFuelType.PETROL)
                .vehicleTransmission(VehicleTransmission.AUTOMATIC)
                .seatingCapacity(5)
                .dailyRate(dailyRate)
                .status(status)
                .imageUrl("https://example.com/camry.jpg")
                .build();
    }
}
