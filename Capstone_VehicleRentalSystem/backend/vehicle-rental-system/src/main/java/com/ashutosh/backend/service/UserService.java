package com.ashutosh.backend.service;

import com.ashutosh.backend.dto.request.RegisterRequestDTO;
import com.ashutosh.backend.dto.request.LoginRequestDTO;
import com.ashutosh.backend.dto.response.LoginResponseDTO;
import com.ashutosh.backend.dto.response.UserResponseDTO;
import com.ashutosh.backend.entity.AppUser;
import com.ashutosh.backend.enums.UserRole;
import com.ashutosh.backend.repository.AppUserRepository;
import com.ashutosh.backend.security.JwtService;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class UserService {

    private final AppUserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;

    // Constructor Injection (Best Practice)
    public UserService(AppUserRepository userRepository, PasswordEncoder passwordEncoder, JwtService jwtService) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtService = jwtService;
    }

    @Transactional
    public UserResponseDTO registerUser(RegisterRequestDTO request) {

        // Sanitize input
        String sanitizedEmail = request.getEmail().toLowerCase().trim();
        request.setEmail(sanitizedEmail); // Update the request object so the clean email is used everywhere below

        // Business Validation: Prevent duplicate accounts
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new RuntimeException("Email is already registered");
        }

        // If you mapped this method in your repository, uncomment it!
        if (userRepository.existsByDriversLicenseNumber(request.getDriversLicenseNumber())) {
            throw new RuntimeException("Driver's license is already registered");
        }

        // Cryptography: Secure the password before saving
        String hashedPassword = passwordEncoder.encode(request.getPassword());

        // Entity Creation
        AppUser newUser = AppUser.builder()
                .firstName(request.getFirstName())
                .lastName(request.getLastName())
                .email(request.getEmail())
                .passwordHash(hashedPassword)
                .phoneNumber(request.getPhoneNumber())
                .driversLicenseNumber(request.getDriversLicenseNumber())
                .role(UserRole.USER) // Every new signup defaults to a standard USER
                .isActive(true)  // Account is active upon creation
                .build();

        // Save and return clean DTO
        AppUser savedUser = userRepository.save(newUser);
        return mapToUserResponseDTO(savedUser);
    }

    public LoginResponseDTO authenticateUser(LoginRequestDTO request) {
        // Find user by email
        AppUser user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new RuntimeException("Invalid email or password"));

        // Senior Safeguard: Block deactivated/banned users from logging in
        if (!user.getIsActive()) {
            throw new RuntimeException("Account has been deactivated. Please contact support.");
        }

        // Verify the raw password against the hashed database password
        if (!passwordEncoder.matches(request.getPassword(), user.getPasswordHash())) {
            throw new RuntimeException("Invalid email or password");
        }

        // Generate the real cryptographic JWT token
        String jwtToken = jwtService.generateToken(user);

        // Return the composed payload for the Frontend UI
        return LoginResponseDTO.builder()
                .token(jwtToken)
                .user(mapToUserResponseDTO(user))
                .build();
    }

    // Helper method to keep our mapping DRY (Don't Repeat Yourself)
    private UserResponseDTO mapToUserResponseDTO(AppUser user) {
        return UserResponseDTO.builder()
                .id(user.getId())
                .firstName(user.getFirstName())
                .lastName(user.getLastName())
                .email(user.getEmail())
                .phoneNumber(user.getPhoneNumber())
                .role(user.getRole()) // Assuming your DTO expects a String here, otherwise remove .name()
                .isActive(user.getIsActive())
                .build();
    }
}