package com.ashutosh.backend.dto.response;

import com.ashutosh.backend.enums.VehicleFuelType;
import com.ashutosh.backend.enums.VehicleStatus;
import com.ashutosh.backend.enums.VehicleTransmission;
import com.ashutosh.backend.enums.VehicleType;
import lombok.Builder;
import lombok.Data;
import java.math.BigDecimal;

/**
 * Data Transfer Object for presenting vehicle details to the client application.
 * This class serves as the primary data structure for populating the vehicle catalog,
 * providing users with all necessary technical specifications and current availability
 * status for browsing and selection.
 */
@Data
@Builder
public class VehicleResponseDTO {
    private Long id;
    private String make;
    private String model;
    private String licensePlate;
    private VehicleType vehicleType;
    private VehicleFuelType vehicleFuelType;
    private VehicleTransmission vehicleTransmission;
    private Integer seatingCapacity;
    private BigDecimal dailyRate;
    private VehicleStatus status;

    /**
     * The stored URL for the vehicle's display image used in the frontend catalog.
     */
    private String imageUrl;
}
