package com.ashutosh.backend.config;

import com.ashutosh.backend.entity.AppUser;
import com.ashutosh.backend.enums.UserRole;
import com.ashutosh.backend.repository.AppUserRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.crypto.password.PasswordEncoder;

/**
 * Automatically adds initial data to the database when the app starts.
 * Ensures an admin account is always available for testing and system management.
 */
@Configuration
public class DataSeeder {

    /**
     * Seeds a default admin account if it does not already exist.
     * Checks for the admin email to prevent duplicate entries and secure
     * the password using the provided encoder.
     *
     * @param userRepository The repository used to check for and save the user.
     * @param passwordEncoder The component used to hash the default password.
     * @return A runner that executes the seeding logic during startup.
     */
    @Bean
    CommandLineRunner initDatabase(AppUserRepository userRepository, PasswordEncoder passwordEncoder) {
        return args -> {
            if (!userRepository.existsByEmail("admin@test.com")) {
                AppUser admin = AppUser.builder()
                        .firstName("Admin")
                        .lastName("User")
                        .email("admin@test.com")
                        .passwordHash(passwordEncoder.encode("admin123"))
                        .phoneNumber("9999999999")
                        .driversLicenseNumber("ADMIN12345")
                        .role(UserRole.ADMIN)
                        .isActive(true)
                        .build();
                userRepository.save(admin);
                System.out.println("Admin account seeded successfully.");
            } else {
                System.out.println(" Admin already exists, skipping seeding");
            }
        };
    }
}