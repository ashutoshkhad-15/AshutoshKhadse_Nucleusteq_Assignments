package com.ashutosh.backend.dto.request;

import com.ashutosh.backend.enums.VehicleFuelType;
import com.ashutosh.backend.enums.VehicleStatus;
import com.ashutosh.backend.enums.VehicleTransmission;
import com.ashutosh.backend.enums.VehicleType;
import jakarta.validation.constraints.*;
import lombok.Data;
import java.math.BigDecimal;

/**
 * Data Transfer Object for creating or updating vehicle records.
 * Used by administrative roles to manage the fleet inventory, ensuring all
 * technical specifications and pricing details meet system requirements.
 */
@Data
public class VehicleRequestDTO {

    /**
     * The manufacturer of the vehicle (e.g., BMW, Mahindra).
     */
    @NotBlank(message = "Make cannot be blank")
    @Size(min = 2, max = 50, message = "Make must be between 2 and 50 characters")
    private String make;

    /**
     * The specific model name of the vehicle.
     */
    @NotBlank(message = "Model cannot be blank")
    @Size(min = 1, max = 100, message = "Model must be between 1 and 100 characters")
    private String model;

    /**
     * The unique legal identifier for the vehicle.
     * Enforces a strictly alphanumeric format with hyphens.
     */
    @NotBlank(message = "License plate cannot be blank")
    @Pattern(regexp = "^[A-Z0-9-]+$", message = "License plate must contain only uppercase letters and numbers and hyphens")
    private String licensePlate;

    /**
     * Categorizes the vehicle as a CAR or BIKE.
     */
    @NotNull(message = "Vehicle type is required")
    private VehicleType vehicleType;

    /**
     * Specifies the engine or energy source technology.
     */
    @NotNull(message = "Fuel type is required")
    private VehicleFuelType vehicleFuelType;

    /**
     * Indicates whether the vehicle is Manual or Automatic.
     */
    @NotNull(message = "Transmission is required")
    private VehicleTransmission vehicleTransmission;

    /**
     * The current operational status of the vehicle.
     */
    private VehicleStatus status;

    /**
     * The total number of passengers the vehicle can legally carry.
     */
    @NotNull(message = "Seating capacity is required")
    @Min(value = 1, message = "Seating capacity must be at least 1")
    @Max(value = 60, message = "Seating capacity cannot exceed 60")
    private Integer seatingCapacity;

    /**
     * The rental cost per day.
     * Validates that the amount is positive and follows standard currency precision.
     */
    @NotNull(message = "Daily rate is required")
    @DecimalMin(value = "0.0", inclusive = false, message = "Daily rate must be strictly greater than zero")
    @Digits(integer = 8, fraction = 2, message = "Daily rate format is invalid (must have up to 2 decimal places)")
    private BigDecimal dailyRate;

    /**
     * Optional link to a hosted image of the vehicle for display in the catalog.
     */
    @Size(max = 500, message = "Image URL cannot exceed 500 characters")
    private String imageUrl;
}