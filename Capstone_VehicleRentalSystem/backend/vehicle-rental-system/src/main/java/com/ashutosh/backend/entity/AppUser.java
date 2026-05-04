package com.ashutosh.backend.entity;

import com.ashutosh.backend.enums.UserRole;
import jakarta.persistence.*;
import lombok.*;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.LocalDateTime;

/**
 * Represents a registered user within the system.
 * This entity serves as the core identity model, managing authentication credentials,
 * user roles, and personal contact information. It utilizes JPA auditing to
 * track account lifecycle events.
 */
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Entity
@Table(name = "app_users")
@EntityListeners(AuditingEntityListener.class)
public class AppUser {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "first_name", nullable = false)
    private String firstName;

    @Column(name = "last_name", nullable = false)
    private String lastName;

    @Column(unique = true, nullable = false)
    private String email;

    @Column(name = "phone_number", unique = true)
    private String phoneNumber;

    /**
     * The cryptographically hashed version of the user's password.
     * Raw passwords are never stored directly in the database to ensure security.
     */
    @Column(name = "password_hash", nullable = false)
    private String passwordHash;

    /**
     * The assigned access level determining the user's permissions.
     * Stored as a string in the database for better readability during manual audits.
     */
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private UserRole role = UserRole.USER;

    @Column(name = "drivers_license_number", unique = true)
    private String driversLicenseNumber;

    @Column(name = "is_active")
    private Boolean isActive = true;

    @CreatedDate
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    /**
     * The timestamp of the most recent update to the user's profile.
     */
    @LastModifiedDate
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
}