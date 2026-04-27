package com.ashutosh.backend.dto.request;

import com.ashutosh.backend.enums.VehicleFuelType;
import com.ashutosh.backend.enums.VehicleStatus;
import com.ashutosh.backend.enums.VehicleTransmission;
import com.ashutosh.backend.enums.VehicleType;
import jakarta.validation.constraints.*;
import lombok.Data;
import java.math.BigDecimal;

@Data
public class VehicleRequestDTO {
    // Used when an Admin adds or updates a car.
    @NotBlank(message = "Make cannot be blank")
    @Size(min = 2, max = 50, message = "Make must be between 2 and 50 characters")
    private String make;

    @NotBlank(message = "Model cannot be blank")
    @Size(min = 1, max = 100, message = "Model must be between 1 and 100 characters")
    private String model;

    @NotBlank(message = "License plate cannot be blank")
    @Pattern(regexp = "^[A-Z0-9-]+$", message = "License plate must contain only uppercase letters and numbers and hyphens")
    private String licensePlate;

    @NotNull(message = "Vehicle type is required")
    private VehicleType vehicleType;

    @NotNull(message = "Fuel type is required")
    private VehicleFuelType vehicleFuelType;

    @NotNull(message = "Transmission is required")
    private VehicleTransmission vehicleTransmission;

    private VehicleStatus status;

    @NotNull(message = "Seating capacity is required")
    @Min(value = 1, message = "Seating capacity must be at least 1")
    @Max(value = 60, message = "Seating capacity cannot exceed 60")
    private Integer seatingCapacity;

    @NotNull(message = "Daily rate is required")
    @DecimalMin(value = "0.0", inclusive = false, message = "Daily rate must be strictly greater than zero")
    @Digits(integer = 8, fraction = 2, message = "Daily rate format is invalid (must have up to 2 decimal places)")
    private BigDecimal dailyRate;

    @Size(max = 500, message = "Image URL cannot exceed 500 characters")
    private String imageUrl;
}
