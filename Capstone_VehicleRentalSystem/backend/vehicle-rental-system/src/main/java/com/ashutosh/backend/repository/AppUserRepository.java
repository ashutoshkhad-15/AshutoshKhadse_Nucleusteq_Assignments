package com.ashutosh.backend.repository;

import com.ashutosh.backend.entity.AppUser;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;

/**
 * Data access interface for managing User entities.
 * Provides methods to query user information from the database for authentication and registration.
 */
@Repository
public interface AppUserRepository extends JpaRepository<AppUser, Long> {

    /**
     * Retrieves a user based on their unique email address.
     * Primarily used during the login process to verify user credentials.
     *
     * @param email The email address to search for.
     * @return An Optional containing the user if found.
     */
    Optional<AppUser> findByEmail(String email);

    /**
     * Checks if an email address is already registered in the system.
     * Used during registration to prevent duplicate accounts.
     *
     * @param email The email address to validate.
     * @return True if the email exists, false otherwise.
     */
    boolean existsByEmail(String email);

    /**
     * Verifies if a driver's license number is already associated with an account.
     * Ensures that each license number is unique across the platform for legal compliance.
     *
     * @param driversLicenseNumber The license number to check.
     * @return True if the license number exists, false otherwise.
     */
    boolean existsByDriversLicenseNumber(String driversLicenseNumber);
}