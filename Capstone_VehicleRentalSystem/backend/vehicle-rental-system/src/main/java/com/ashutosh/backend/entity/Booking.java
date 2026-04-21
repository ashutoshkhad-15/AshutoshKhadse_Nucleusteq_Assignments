package com.ashutosh.backend.entity;

import com.ashutosh.backend.enums.BookingStatus;
import jakarta.persistence.*;
import lombok.*;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

// I've designed this entity to be the "bridge" between our Users and our Vehicles.
// This is where the actual business value of the Vehicle Rental System lives
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Entity
@Table(name = "bookings")
@EntityListeners(AuditingEntityListener.class)
public class Booking {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // I chose @ManyToOne for the User relationship.
    // I set fetch = FetchType.LAZY because I learned that we don't always need to
    // pull all user profile details just to see a booking list, this saves on performance.
    // Also, setting optional = false ensures a booking can never exist without a valid user.
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "user_id", nullable = false)
    private AppUser user;

    // Similarly, a booking must have a vehicle.
    // I kept this unidirectional for now to keep the code simpler and avoid
    // infinite recursion issues during JSON serialization later on.
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "vehicle_id", nullable = false)
    private Vehicle vehicle;

    // I used LocalDate here instead of LocalDateTime because, for a rental system,
    // we usually care about the "Days" rather than the specific seconds of the booking.
    @Column(name = "start_date", nullable = false)
    private LocalDate startDate;

    @Column(name = "end_date", nullable = false)
    private LocalDate endDate;

    // I'm capturing the price_per_day at the MOMENT of booking.
    // I learned that if we change the vehicle's rate in the 'vehicles' table later,
    // it shouldn't change the historical price the customer already agreed to
    @Column(name = "price_per_day", nullable = false)
    private BigDecimal pricePerDay;

    @Column(name = "total_amount", nullable = false)
    private BigDecimal totalAmount;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private BookingStatus status = BookingStatus.PENDING;

    // Just like in the Vehicle entity, I'm using @Version to handle
    // concurrent booking attempts gracefully.
    @Version
    private Integer version;

    @CreatedDate
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
}