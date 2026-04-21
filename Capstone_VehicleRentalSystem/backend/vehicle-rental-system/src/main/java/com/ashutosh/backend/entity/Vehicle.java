package com.ashutosh.backend.entity;

import com.ashutosh.backend.enums.VehicleStatus;
import com.ashutosh.backend.enums.VehicleType;
import jakarta.persistence.*;
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

    // Basic identifiers for the vehicle.
    @Column(nullable = false)
    private String make;

    @Column(nullable = false)
    private String model;

    // License plate must be unique, we can't have two different cars with the same plate in our system
    @Column(name = "license_plate", unique = true, nullable = false)
    private String licensePlate;

    // Using STRING enums so "CAR", "BIKE" is readable in the database tables.
    @Enumerated(EnumType.STRING)
    @Column(name = "vehicle_type", nullable = false)
    private VehicleType vehicleType;

    @Column(name = "fuel_type")
    private String fuelType;

    private String transmission;

    @Column(name = "seating_capacity")
    private Integer seatingCapacity = 4;

    // I used BigDecimal for the daily rate.
    // I read that using 'Double' for financial data is a bad practice because of
    // floating-point precision issues. BigDecimal ensures we don't lose a single rupee
    @Column(name = "daily_rate", nullable = false)
    private BigDecimal dailyRate;

    // Tracks if the vehicle is AVAILABLE, BOOKED, RETIRED or UNDER_MAINTENANCE.
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private VehicleStatus status = VehicleStatus.AVAILABLE;

    // I added this feature to give the user a realistic feel while using the project
    // Storing a link to the image rather than the image itself
    // to keep the database size optimized.
    // I will add the images in the project folder currently working on that part
    @Column(name = "image_url")
    private String imageUrl;

    // I added the @Version field here. I learned that in a high-concurrency
    // environment like multiple people trying to book the last available car,
    // this prevents "lost updates" without needing to lock the whole database table.
    @Version
    private Integer version;

    @CreatedDate
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
}
