package com.ashutosh.backend.dto.response;

import com.ashutosh.backend.enums.VehicleFuelType;
import com.ashutosh.backend.enums.VehicleStatus;
import com.ashutosh.backend.enums.VehicleTransmission;
import com.ashutosh.backend.enums.VehicleType;
import lombok.Builder;
import lombok.Data;
import java.math.BigDecimal;

@Data
@Builder
public class VehicleResponseDTO {
    // Sent to the frontend so users can see the catalog and available cars.
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
    private String imageUrl;
}
