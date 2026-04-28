package com.ashutosh.backend.service;

import com.ashutosh.backend.dto.request.RegisterRequestDTO;
import com.ashutosh.backend.dto.request.LoginRequestDTO;
import com.ashutosh.backend.dto.response.LoginResponseDTO;
import com.ashutosh.backend.dto.response.UserResponseDTO;
import com.ashutosh.backend.entity.AppUser;
import com.ashutosh.backend.enums.UserRole;
import com.ashutosh.backend.exception.DuplicateResourceException;
import com.ashutosh.backend.exception.InvalidCredentialsException;
import com.ashutosh.backend.exception.ResourceNotFoundException;
import com.ashutosh.backend.repository.AppUserRepository;
import com.ashutosh.backend.security.JwtService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Service class responsible for managing user accounts.
 * Handles the business logic for user registration, login authentication, and profile retrieval.
 */
@Service
@Slf4j
public class UserService {

    private final AppUserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;

    /**
     * Constructor used to inject required dependencies like the repository and security services.
     */
    public UserService(AppUserRepository userRepository, PasswordEncoder passwordEncoder, JwtService jwtService) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtService = jwtService;
    }

    /**
     * Registers a new user in the system.
     * Validates that the email and license are unique, hashes the password,
     * and persists the record to the database.
     *
     * @param request The data transfer object containing the user's signup details.
     * @return UserResponseDTO The newly created user details.
     */
    @Transactional
    public UserResponseDTO registerUser(RegisterRequestDTO request) {

        // Formats the email to lowercase to prevent case-sensitive login issues
        String sanitizedEmail = request.getEmail().toLowerCase().trim();
        request.setEmail(sanitizedEmail);

        log.info("Starting registration process for new email: {}", sanitizedEmail);

        // Validates database constraints to prevent duplicate accounts
        if (userRepository.existsByEmail(request.getEmail())) {
            log.warn("Registration failed: The email {} is already registered in the database.", request.getEmail());
            throw new DuplicateResourceException("Email is already registered");
        }

        if (userRepository.existsByDriversLicenseNumber(request.getDriversLicenseNumber())) {
            log.warn("Registration failed: Driver's license {} is already linked to an account.", request.getDriversLicenseNumber());
            throw new DuplicateResourceException("Driver's license is already registered");
        }

        // Hashes the password using Spring Security
        String hashedPassword = passwordEncoder.encode(request.getPassword());

        // Constructs the new AppUser entity
        AppUser newUser = AppUser.builder()
                .firstName(request.getFirstName())
                .lastName(request.getLastName())
                .email(request.getEmail())
                .passwordHash(hashedPassword)
                .phoneNumber(request.getPhoneNumber())
                .driversLicenseNumber(request.getDriversLicenseNumber())
                .role(UserRole.USER) // Assigns standard user role by default
                .isActive(true)      // Activates the account immediately upon creation
                .build();

        // Persists the entity and returns the safe response DTO
        AppUser savedUser = userRepository.save(newUser);
        log.info("Successfully registered new user with ID: {}", savedUser.getId());

        return mapToUserResponseDTO(savedUser);
    }

    /**
     * Fetches the profile details of an existing user using their email address.
     *
     * @param email The email of the user to look up.
     * @return UserResponseDTO The user's profile data.
     */
    public UserResponseDTO getUserProfile(String email) {
        log.info("Fetching profile data for user email: {}", email);

        AppUser user = userRepository.findByEmail(email)
                .orElseThrow(() -> {
                    log.error("Profile fetch failed: No user record found for email: {}", email);
                    return new ResourceNotFoundException("User not found");
                });

        return mapToUserResponseDTO(user);
    }

    /**
     * Authenticates a user's login attempt.
     * Verifies the email, checks the hashed password, and generates a JWT token upon success.
     *
     * @param request The login credentials provided by the user.
     * @return LoginResponseDTO An object containing the JWT token and user details.
     */
    public LoginResponseDTO authenticateUser(LoginRequestDTO request) {
        String sanitizedEmail = request.getEmail().toLowerCase().trim();
        log.info("Authentication attempt started for email: {}", sanitizedEmail);

        // Searches for the user in the database
        AppUser user = userRepository.findByEmail(sanitizedEmail)
                .orElseThrow(() -> {
                    log.warn("Login failed: Email {} not found in the system.", sanitizedEmail);
                    return new InvalidCredentialsException("Invalid email or password");
                });

        // Ensures the account has not been deactivated or banned
        if (!user.getIsActive()) {
            log.warn("Login blocked: The account associated with {} is deactivated.", sanitizedEmail);
            throw new InvalidCredentialsException("Account has been deactivated. Please contact support.");
        }

        // Verifies the provided password against the hashed password stored in the database
        if (!passwordEncoder.matches(request.getPassword(), user.getPasswordHash())) {
            log.warn("Login failed: Incorrect password provided for email {}.", sanitizedEmail);
            throw new InvalidCredentialsException("Invalid email or password");
        }

        // Generates the JWT token for the user's session
        String jwtToken = jwtService.generateToken(user);
        log.info("Successfully authenticated user: {}. JWT token generated.", sanitizedEmail);

        // Returns the payload required by the frontend application
        return LoginResponseDTO.builder()
                .token(jwtToken)
                .user(mapToUserResponseDTO(user))
                .build();
    }

    /**
     * Helper method to map an AppUser database entity to a UserResponseDTO.
     * Ensures sensitive fields like passwords are not exposed to the frontend.
     *
     * @param user The database entity.
     * @return UserResponseDTO The safe response object.
     */
    private UserResponseDTO mapToUserResponseDTO(AppUser user) {
        return UserResponseDTO.builder()
                .id(user.getId())
                .firstName(user.getFirstName())
                .lastName(user.getLastName())
                .email(user.getEmail())
                .phoneNumber(user.getPhoneNumber())
                .role(user.getRole())
                .isActive(user.getIsActive())
                .build();
    }
}