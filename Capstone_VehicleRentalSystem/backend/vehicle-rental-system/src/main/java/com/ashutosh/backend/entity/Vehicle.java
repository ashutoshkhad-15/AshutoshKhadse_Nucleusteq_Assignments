package com.ashutosh.backend.entity;

import com.ashutosh.backend.enums.VehicleStatus;
import com.ashutosh.backend.enums.VehicleType;
import com.ashutosh.backend.enums.VehicleTransmission;
import com.ashutosh.backend.enums.VehicleFuelType;
import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import lombok.*;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.math.BigDecimal;
import java.time.LocalDateTime;

// I'm using the Lombok and JPA Auditing approach
// It keeps our database schema consistent and our Java code clean.
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Entity
@Table(name = "vehicles")
@EntityListeners(AuditingEntityListener.class)
public class Vehicle {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // @NotBlank ensures the string is not null, not empty, and doesn't contain only spaces.
    // @Size limits the length to prevent malicious massive string injections.
    @NotBlank(message = "Make cannot be blank")
    @Size(min = 2, max = 50, message = "Make must be between 2 and 50 characters")
    @Column(nullable = false, length = 50)
    private String make;

    @NotBlank(message = "Model cannot be blank")
    @Size(min = 1, max = 100, message = "Model must be between 1 and 100 characters")
    @Column(nullable = false, length = 100)
    private String model;

    // License plate must be unique, we can't have two different cars with the same plate in our system
    // @Pattern uses a Regular Expression (Regex) to ensure only valid license plate characters are allowed.
    @NotBlank(message = "License plate cannot be blank")
    @Pattern(regexp = "^[A-Z0-9]+$", message = "License plate must contain only uppercase letters, numbers")
    @Column(name = "license_plate", unique = true, nullable = false, length = 20)
    private String licensePlate;

    // Using STRING enums so "CAR", "BIKE" is readable in the database tables.
    @NotNull(message = "Vehicle type is required")
    @Enumerated(EnumType.STRING)
    @Column(name = "vehicle_type", nullable = false, length = 20)
    private VehicleType vehicleType;

    @NotNull(message = "Fuel type is required")
    @Enumerated(EnumType.STRING)
    @Column(name = "fuel_type", nullable = false, length = 30)
    private VehicleFuelType vehicleFuelType;

    @NotNull(message = "Transmission is required")
    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    private VehicleTransmission  vehicleTransmission;

    @NotNull(message = "Seating capacity is required")
    @Min(value = 1, message = "Seating capacity must be at least 1")
    @Max(value = 60, message = "Seating capacity cannot exceed 60")
    @Column(name = "seating_capacity", nullable = false)
    private Integer seatingCapacity = 4;

    // @DecimalMin prevents negative pricing.
    // @Digits strictly enforces the precision (max 8 digits before decimal, max 2 after).
    @NotNull(message = "Daily rate is required")
    @DecimalMin(value = "0.0", inclusive = false, message = "Daily rate must be strictly greater than zero")
    @Digits(integer = 8, fraction = 2, message = "Daily rate format is invalid (must have up to 2 decimal places)")
    @Column(name = "daily_rate", nullable = false, precision = 10, scale = 2)
    private BigDecimal dailyRate;

    // Tracks if the vehicle is AVAILABLE, BOOKED, RETIRED or UNDER_MAINTENANCE.
    @NotNull(message = "Vehicle status is required")
    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private VehicleStatus status = VehicleStatus.AVAILABLE;

    @Size(max = 500, message = "Image URL cannot exceed 500 characters")
    @Column(name = "image_url", length = 500)
    private String imageUrl;

    @Version
    private Integer version;

    @CreatedDate
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
}
