package com.ashutosh.backend.service;

import com.ashutosh.backend.dto.request.LoginRequestDTO;
import com.ashutosh.backend.dto.request.RegisterRequestDTO;
import com.ashutosh.backend.dto.response.LoginResponseDTO;
import com.ashutosh.backend.dto.response.UserResponseDTO;
import com.ashutosh.backend.entity.AppUser;
import com.ashutosh.backend.enums.UserRole;
import com.ashutosh.backend.exception.DuplicateResourceException;
import com.ashutosh.backend.exception.InvalidCredentialsException;
import com.ashutosh.backend.exception.ResourceNotFoundException;
import com.ashutosh.backend.repository.AppUserRepository;
import com.ashutosh.backend.security.JwtService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

/**
 * Unit tests for the UserService class using Mockito.
 * Tests core business logic including registration validations and authentication flows.
 */
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private AppUserRepository userRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    @Mock
    private JwtService jwtService;

    @InjectMocks
    private UserService userService;

    private AppUser mockUser;
    private RegisterRequestDTO registerRequest;
    private LoginRequestDTO loginRequest;

    @BeforeEach
    void setUp() {
        // Prepare reusable mock data before each test runs
        mockUser = AppUser.builder()
                .id(1L)
                .firstName("John")
                .lastName("Doe")
                .email("john@example.com")
                .passwordHash("hashed_password_123")
                .phoneNumber("1234567890")
                .driversLicenseNumber("DL-12345")
                .role(UserRole.USER)
                .isActive(true)
                .build();

        registerRequest = new RegisterRequestDTO();
        registerRequest.setFirstName("John");
        registerRequest.setLastName("Doe");
        registerRequest.setEmail("john@example.com");
        registerRequest.setPassword("raw_password_123");
        registerRequest.setPhoneNumber("1234567890");
        registerRequest.setDriversLicenseNumber("DL-12345");

        loginRequest = new LoginRequestDTO();
        loginRequest.setEmail("john@example.com");
        loginRequest.setPassword("raw_password_123");
    }

    // 1. REGISTRATION TESTS
    @Test
    void registerUser_Success() {
        // GIVEN: Email and license are unique
        when(userRepository.existsByEmail(anyString())).thenReturn(false);
        when(userRepository.existsByDriversLicenseNumber(anyString())).thenReturn(false);
        when(passwordEncoder.encode(anyString())).thenReturn("hashed_password_123");
        when(userRepository.save(any(AppUser.class))).thenReturn(mockUser);

        // WHEN: We attempt to register
        UserResponseDTO response = userService.registerUser(registerRequest);

        // THEN: Registration succeeds and returns correct mapped data
        assertNotNull(response);
        assertEquals("john@example.com", response.getEmail());
        assertEquals("John", response.getFirstName());
        verify(userRepository, times(1)).save(any(AppUser.class));
    }

    @Test
    void registerUser_DuplicateEmail_ThrowsException() {
        // GIVEN: Email already exists in the database
        when(userRepository.existsByEmail(anyString())).thenReturn(true);

        // WHEN & THEN: Service should throw a DuplicateResourceException
        assertThrows(DuplicateResourceException.class, () -> userService.registerUser(registerRequest));
        verify(userRepository, never()).save(any(AppUser.class)); // Ensure it never tries to save
    }

    @Test
    void registerUser_DuplicateLicense_ThrowsException() {
        // GIVEN: Email is unique, but License already exists
        when(userRepository.existsByEmail(anyString())).thenReturn(false);
        when(userRepository.existsByDriversLicenseNumber(anyString())).thenReturn(true);

        // WHEN & THEN
        assertThrows(DuplicateResourceException.class, () -> userService.registerUser(registerRequest));
        verify(userRepository, never()).save(any(AppUser.class));
    }

    // 2. GET PROFILE TESTS
    @Test
    void getUserProfile_Success() {
        // GIVEN: The user exists
        when(userRepository.findByEmail("john@example.com")).thenReturn(Optional.of(mockUser));

        // WHEN
        UserResponseDTO response = userService.getUserProfile("john@example.com");

        // THEN
        assertNotNull(response);
        assertEquals("john@example.com", response.getEmail());
    }

    @Test
    void getUserProfile_NotFound_ThrowsException() {
        // GIVEN: The user does not exist
        when(userRepository.findByEmail("unknown@example.com")).thenReturn(Optional.empty());

        // WHEN & THEN
        assertThrows(ResourceNotFoundException.class, () -> userService.getUserProfile("unknown@example.com"));
    }

    // 3. AUTHENTICATION (LOGIN) TESTS
    @Test
    void authenticateUser_Success() {
        // GIVEN: Valid user, active account, correct password
        when(userRepository.findByEmail(anyString())).thenReturn(Optional.of(mockUser));
        when(passwordEncoder.matches("raw_password_123", "hashed_password_123")).thenReturn(true);
        when(jwtService.generateToken(mockUser)).thenReturn("fake-jwt-token-string");

        // WHEN
        LoginResponseDTO response = userService.authenticateUser(loginRequest);

        // THEN
        assertNotNull(response);
        assertEquals("fake-jwt-token-string", response.getToken());
        assertEquals("john@example.com", response.getUser().getEmail());
    }

    @Test
    void authenticateUser_WrongPassword_ThrowsException() {
        // GIVEN: Valid user, but password check fails
        when(userRepository.findByEmail(anyString())).thenReturn(Optional.of(mockUser));
        when(passwordEncoder.matches(anyString(), anyString())).thenReturn(false);

        // WHEN & THEN
        assertThrows(InvalidCredentialsException.class, () -> userService.authenticateUser(loginRequest));
        verify(jwtService, never()).generateToken(any(AppUser.class)); // Token should not be generated
    }

    @Test
    void authenticateUser_AccountDeactivated_ThrowsException() {
        // GIVEN: User exists but is inactive
        mockUser.setIsActive(false);
        when(userRepository.findByEmail(anyString())).thenReturn(Optional.of(mockUser));

        // WHEN & THEN
        InvalidCredentialsException exception = assertThrows(InvalidCredentialsException.class, () -> userService.authenticateUser(loginRequest));
        assertTrue(exception.getMessage().contains("deactivated"));
    }
}