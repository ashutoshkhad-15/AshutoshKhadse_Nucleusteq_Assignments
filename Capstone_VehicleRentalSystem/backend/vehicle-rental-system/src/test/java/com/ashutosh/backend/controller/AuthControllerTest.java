package com.ashutosh.backend.controller;

import com.ashutosh.backend.dto.request.LoginRequestDTO;
import com.ashutosh.backend.dto.request.RegisterRequestDTO;
import com.ashutosh.backend.dto.response.LoginResponseDTO;
import com.ashutosh.backend.dto.response.UserResponseDTO;
import com.ashutosh.backend.entity.AppUser;
import com.ashutosh.backend.enums.UserRole;
import com.ashutosh.backend.exception.DuplicateResourceException;
import com.ashutosh.backend.exception.GlobalExceptionHandler;
import com.ashutosh.backend.exception.InvalidCredentialsException;
import com.ashutosh.backend.service.UserService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.MediaType;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.validation.beanvalidation.LocalValidatorFactoryBean;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoMoreInteractions;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@ExtendWith(MockitoExtension.class)
class AuthControllerTest {

    @Mock
    private UserService userService;

    @InjectMocks
    private AuthController authController;

    private MockMvc mockMvc;
    private ObjectMapper objectMapper;
    private RegisterRequestDTO registerRequest;
    private LoginRequestDTO loginRequest;
    private UserResponseDTO userResponse;
    private LoginResponseDTO loginResponse;

    @BeforeEach
    void setUp() {
        LocalValidatorFactoryBean validator = new LocalValidatorFactoryBean();
        validator.afterPropertiesSet();

        mockMvc = MockMvcBuilders.standaloneSetup(authController)
                .setControllerAdvice(new GlobalExceptionHandler())
                .setValidator(validator)
                .build();

        objectMapper = new ObjectMapper();

        registerRequest = new RegisterRequestDTO();
        registerRequest.setFirstName("Ashutosh");
        registerRequest.setLastName("Khadse");
        registerRequest.setEmail("ashutosh@example.com");
        registerRequest.setPassword("secret123");
        registerRequest.setPhoneNumber("9876543210");
        registerRequest.setDriversLicenseNumber("DL12345");

        loginRequest = new LoginRequestDTO();
        loginRequest.setEmail("ashutosh@example.com");
        loginRequest.setPassword("secret123");

        userResponse = UserResponseDTO.builder()
                .id(1L)
                .firstName("Ashutosh")
                .lastName("Khadse")
                .email("ashutosh@example.com")
                .phoneNumber("9876543210")
                .role(UserRole.USER)
                .isActive(true)
                .build();

        loginResponse = LoginResponseDTO.builder()
                .token("jwt-token-value")
                .user(userResponse)
                .build();
    }

    @Test
    void register_ReturnsCreatedUserResponse() throws Exception {
        // GIVEN
        when(userService.registerUser(any(RegisterRequestDTO.class))).thenReturn(userResponse);

        // WHEN
        mockMvc.perform(post("/api/auth/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(registerRequest)))

                // THEN
                .andExpect(status().isOk())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$.id").value(1L))
                .andExpect(jsonPath("$.firstName").value("Ashutosh"))
                .andExpect(jsonPath("$.lastName").value("Khadse"))
                .andExpect(jsonPath("$.email").value("ashutosh@example.com"))
                .andExpect(jsonPath("$.phoneNumber").value("9876543210"))
                .andExpect(jsonPath("$.role").value("USER"))
                .andExpect(jsonPath("$.isActive").value(true));

        ArgumentCaptor<RegisterRequestDTO> captor = ArgumentCaptor.forClass(RegisterRequestDTO.class);
        verify(userService, times(1)).registerUser(captor.capture());
        RegisterRequestDTO capturedRequest = captor.getValue();
        assertNotNull(capturedRequest);
        assertEquals("Ashutosh", capturedRequest.getFirstName());
        assertEquals("ashutosh@example.com", capturedRequest.getEmail());
        verifyNoMoreInteractions(userService);
    }

    @Test
    void register_WhenRequestIsInvalid_ReturnsBadRequest() throws Exception {
        // GIVEN
        RegisterRequestDTO invalidRequest = new RegisterRequestDTO();
        invalidRequest.setFirstName("A1");
        invalidRequest.setLastName("");
        invalidRequest.setEmail("invalid-email");
        invalidRequest.setPassword("123");
        invalidRequest.setPhoneNumber("12345");
        invalidRequest.setDriversLicenseNumber("dl");

        // WHEN
        mockMvc.perform(post("/api/auth/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(invalidRequest)))

                // THEN
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.status").value(400))
                .andExpect(jsonPath("$.errors.firstName").exists())
                .andExpect(jsonPath("$.errors.lastName").exists())
                .andExpect(jsonPath("$.errors.email").exists())
                .andExpect(jsonPath("$.errors.password").value("Password must be at least 6 characters long"))
                .andExpect(jsonPath("$.errors.phoneNumber").value("Phone number must be exactly 10 digits"))
                .andExpect(jsonPath("$.errors.driversLicenseNumber").exists());

        verify(userService, never()).registerUser(any(RegisterRequestDTO.class));
    }

    @Test
    void register_WhenServiceThrowsDuplicateResourceException_ReturnsConflict() throws Exception {
        // GIVEN
        when(userService.registerUser(any(RegisterRequestDTO.class)))
                .thenThrow(new DuplicateResourceException("Email is already registered"));

        // WHEN
        mockMvc.perform(post("/api/auth/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(registerRequest)))

                // THEN
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.status").value(409))
                .andExpect(jsonPath("$.error").value("Email is already registered"));

        verify(userService, times(1)).registerUser(any(RegisterRequestDTO.class));
    }

    @Test
    void login_ReturnsJwtAndUserResponse() throws Exception {
        // GIVEN
        when(userService.authenticateUser(any(LoginRequestDTO.class))).thenReturn(loginResponse);

        // WHEN
        mockMvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(loginRequest)))

                // THEN
                .andExpect(status().isOk())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$.token").value("jwt-token-value"))
                .andExpect(jsonPath("$.user.id").value(1L))
                .andExpect(jsonPath("$.user.firstName").value("Ashutosh"))
                .andExpect(jsonPath("$.user.email").value("ashutosh@example.com"))
                .andExpect(jsonPath("$.user.role").value("USER"))
                .andExpect(jsonPath("$.user.isActive").value(true));

        ArgumentCaptor<LoginRequestDTO> captor = ArgumentCaptor.forClass(LoginRequestDTO.class);
        verify(userService, times(1)).authenticateUser(captor.capture());
        LoginRequestDTO capturedRequest = captor.getValue();
        assertEquals("ashutosh@example.com", capturedRequest.getEmail());
        assertEquals("secret123", capturedRequest.getPassword());
        verifyNoMoreInteractions(userService);
    }

    @Test
    void login_WhenRequestIsInvalid_ReturnsBadRequest() throws Exception {
        // GIVEN
        LoginRequestDTO invalidRequest = new LoginRequestDTO();
        invalidRequest.setEmail("not-an-email");
        invalidRequest.setPassword("");

        // WHEN
        mockMvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(invalidRequest)))

                // THEN
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.status").value(400))
                .andExpect(jsonPath("$.errors.email").value("Invalid email format"))
                .andExpect(jsonPath("$.errors.password").value("Password is required"));

        verify(userService, never()).authenticateUser(any(LoginRequestDTO.class));
    }

    @Test
    void login_WhenServiceThrowsInvalidCredentialsException_ReturnsUnauthorized() throws Exception {
        // GIVEN
        when(userService.authenticateUser(any(LoginRequestDTO.class)))
                .thenThrow(new InvalidCredentialsException("Invalid email or password"));

        // WHEN
        mockMvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(loginRequest)))

                // THEN
                .andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.status").value(401))
                .andExpect(jsonPath("$.error").value("Invalid email or password"));

        verify(userService, times(1)).authenticateUser(any(LoginRequestDTO.class));
    }

    @Test
    void getCurrentUser_WithAppUserPrincipal_ReturnsUserProfile() throws Exception {
        // GIVEN
        AppUser principal = AppUser.builder()
                .id(1L)
                .email("ashutosh@example.com")
                .build();
        UsernamePasswordAuthenticationToken authentication =
                new UsernamePasswordAuthenticationToken(principal, null);
        when(userService.getUserProfile("ashutosh@example.com")).thenReturn(userResponse);

        // WHEN
        mockMvc.perform(get("/api/auth/me").principal(authentication))

                // THEN
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1L))
                .andExpect(jsonPath("$.email").value("ashutosh@example.com"))
                .andExpect(jsonPath("$.role").value("USER"));

        verify(userService, times(1)).getUserProfile("ashutosh@example.com");
    }

    @Test
    void getCurrentUser_WithUserDetailsPrincipal_ReturnsUserProfile() throws Exception {
        // GIVEN
        UserDetails principal = User.withUsername("details@example.com")
                .password("secret123")
                .roles("USER")
                .build();
        UsernamePasswordAuthenticationToken authentication =
                new UsernamePasswordAuthenticationToken(principal, null, principal.getAuthorities());
        UserResponseDTO detailsUserResponse = UserResponseDTO.builder()
                .id(2L)
                .firstName("Details")
                .lastName("User")
                .email("details@example.com")
                .phoneNumber("1234567890")
                .role(UserRole.USER)
                .isActive(true)
                .build();
        when(userService.getUserProfile("details@example.com")).thenReturn(detailsUserResponse);

        // WHEN
        mockMvc.perform(get("/api/auth/me").principal(authentication))

                // THEN
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(2L))
                .andExpect(jsonPath("$.email").value("details@example.com"));

        verify(userService, times(1)).getUserProfile("details@example.com");
    }

    @Test
    void getCurrentUser_WithStringPrincipal_ReturnsUserProfile() throws Exception {
        // GIVEN
        UsernamePasswordAuthenticationToken authentication =
                new UsernamePasswordAuthenticationToken("stringprincipal@example.com", null);
        UserResponseDTO stringUserResponse = UserResponseDTO.builder()
                .id(3L)
                .firstName("String")
                .lastName("Principal")
                .email("stringprincipal@example.com")
                .phoneNumber("9999999999")
                .role(UserRole.USER)
                .isActive(true)
                .build();
        when(userService.getUserProfile("stringprincipal@example.com")).thenReturn(stringUserResponse);

        // WHEN
        mockMvc.perform(get("/api/auth/me").principal(authentication))

                // THEN
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(3L))
                .andExpect(jsonPath("$.email").value("stringprincipal@example.com"));

        verify(userService, times(1)).getUserProfile("stringprincipal@example.com");
    }
}
