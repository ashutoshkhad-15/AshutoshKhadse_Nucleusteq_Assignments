package com.ashutosh.backend.entity;

import com.ashutosh.backend.enums.UserRole;
import jakarta.persistence.*;
import lombok.*;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.LocalDateTime;

// I used Lombok annotations here @Getter, @Setter, etc. to keep the entity file
// clean and avoid hundreds of lines of boilerplate getters and setters.
// I also added @Builder because it makes creating test users in our unit tests
// much more readable than using a massive constructor
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Entity
// I avoided the table name "users" because it's a reserved keyword in many databases like PostgreSQL.
@Table(name = "app_users")
@EntityListeners(AuditingEntityListener.class) // This is a feature I found for automatic timestamp management.
public class AppUser {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // I ensured nullable = false for mandatory fields to enforce data integrity
    // at the database level, not just the application level.
    @Column(name = "first_name", nullable = false)
    private String firstName;

    @Column(name = "last_name", nullable = false)
    private String lastName;

    // Email and Phone must be unique to prevent duplicate accounts.
    @Column(unique = true, nullable = false)
    private String email;

    @Column(name = "phone_number", unique = true)
    private String phoneNumber;

    // I named this 'passwordHash' to remind myself that i
    // should NEVER store plain-text passwords.
    @Column(name = "password_hash", nullable = false)
    private String passwordHash;

    // I used EnumType.STRING so that in the DB we see "ADMIN" or "USER"
    // instead of just numbers (0, 1)
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private UserRole role = UserRole.USER;

    // For id proof we need this from customers.
    @Column(name = "drivers_license_number", unique = true)
    private String driversLicenseNumber;

    // I added a 'soft delete' flag. Instead of deleting a user and losing history,
    // we can just set isActive = false.
    @Column(name = "is_active")
    private Boolean isActive = true;

    // These annotations work with AuditingEntityListener to automatically
    // fill timestamps whenever a record is created or updated.
    @CreatedDate
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @LastModifiedDate
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
}
