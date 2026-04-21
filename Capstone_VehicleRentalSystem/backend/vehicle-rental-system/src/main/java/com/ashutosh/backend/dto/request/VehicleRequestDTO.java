package com.ashutosh.backend.dto.request;

import com.ashutosh.backend.enums.VehicleType;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import java.math.BigDecimal;

@Data
public class VehicleRequestDTO {
    // Used when an Admin adds or updates a car.
    @NotBlank(message = "Make is required")
    private String make;

    @NotBlank(message = "Model is required")
    private String model;

    @NotBlank(message = "License plate is required")
    private String licensePlate;

    @NotNull(message = "Vehicle type is required")
    private VehicleType vehicleType;

    private String fuelType;
    private String transmission;
    private Integer seatingCapacity;

    @NotNull(message = "Daily rate is required")
    @Min(value = 0, message = "Rate must be positive")
    private BigDecimal dailyRate;

    private String imageUrl;
}
