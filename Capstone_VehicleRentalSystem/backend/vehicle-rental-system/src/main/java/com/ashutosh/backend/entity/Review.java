package com.ashutosh.backend.entity;

import jakarta.persistence.*;
import lombok.*;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.LocalDateTime;

// I decided to add a Review system because feedback is vital for a rental platform.
// It follows the same auditing and Lombok patterns we've established to maintain
// a clean, professional codebase.
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Entity
@Table(name = "reviews")
@EntityListeners(AuditingEntityListener.class)
public class Review {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // I chose a @OneToOne relationship here because logically, one rental booking
    // should only result in one review. I set 'unique = true' on the JoinColumn
    // to enforce this constraint at the database level.

    // I also used FetchType.LAZY. I'm learning that keeping relationships lazy
    // by default is safer for performance, as it prevents the "N+1 problem"
    // where the database gets hammered with unnecessary joins.
    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "booking_id", nullable = false, unique = true)
    private Booking booking;

    // I'm planning to add validation in the DTO/Service layer later to ensure
    // this rating stays between 1 and 5 stars.
    @Column(nullable = false)
    private Integer rating;

    // Comment is optional, as some users might just want to leave a star rating.
    private String comment;

    @CreatedDate
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
}