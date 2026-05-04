package com.ashutosh.backend.controller;

import com.ashutosh.backend.dto.request.BookingRequestDTO;
import com.ashutosh.backend.dto.response.BookingResponseDTO;
import com.ashutosh.backend.entity.AppUser;
import com.ashutosh.backend.enums.BookingStatus;
import com.ashutosh.backend.enums.UserRole;
import com.ashutosh.backend.enums.VehicleType;
import com.ashutosh.backend.exception.GlobalExceptionHandler;
import com.ashutosh.backend.exception.ResourceNotFoundException;
import com.ashutosh.backend.service.BookingService;
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

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

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
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@ExtendWith(MockitoExtension.class)
class BookingControllerTest {

    @Mock
    private BookingService bookingService;

    @InjectMocks
    private BookingController bookingController;

    private MockMvc mockMvc;
    private ObjectMapper objectMapper;
    private BookingRequestDTO bookingRequest;
    private BookingResponseDTO bookingResponse;
    private BookingResponseDTO cancelledBookingResponse;
    private BookingResponseDTO completedBookingResponse;

    @BeforeEach
    void setUp() {
        LocalValidatorFactoryBean validator = new LocalValidatorFactoryBean();
        validator.afterPropertiesSet();

        mockMvc = MockMvcBuilders.standaloneSetup(bookingController)
                .setControllerAdvice(new GlobalExceptionHandler())
                .setValidator(validator)
                .build();

        objectMapper = new ObjectMapper().findAndRegisterModules();

        bookingRequest = new BookingRequestDTO();
        bookingRequest.setVehicleId(100L);
        bookingRequest.setStartDate(LocalDate.now().plusDays(1));
        bookingRequest.setEndDate(LocalDate.now().plusDays(3));

        bookingResponse = buildBookingResponse(500L, "ashutosh@example.com", BookingStatus.CONFIRMED, false);
        cancelledBookingResponse = buildBookingResponse(500L, "ashutosh@example.com", BookingStatus.CANCELLED, false);
        completedBookingResponse = buildBookingResponse(500L, "ashutosh@example.com", BookingStatus.COMPLETED, true);
    }

    @Test
    void createBooking_ReturnsCreatedBooking() throws Exception {
        // GIVEN
        AppUser principal = AppUser.builder()
                .id(1L)
                .email("ashutosh@example.com")
                .role(UserRole.USER)
                .build();
        UsernamePasswordAuthenticationToken authentication =
                new UsernamePasswordAuthenticationToken(principal, null);
        when(bookingService.createBooking(any(BookingRequestDTO.class), any(String.class))).thenReturn(bookingResponse);

        // WHEN
        mockMvc.perform(post("/api/bookings")
                        .principal(authentication)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(bookingRequest)))

                // THEN
                .andExpect(status().isCreated())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$.id").value(500L))
                .andExpect(jsonPath("$.userEmail").value("ashutosh@example.com"))
                .andExpect(jsonPath("$.vehicleId").value(100L))
                .andExpect(jsonPath("$.vehicleName").value("Toyota Camry"))
                .andExpect(jsonPath("$.vehicleType").value("CAR"))
                .andExpect(jsonPath("$.startDate[0]").value(bookingRequest.getStartDate().getYear()))
                .andExpect(jsonPath("$.startDate[1]").value(bookingRequest.getStartDate().getMonthValue()))
                .andExpect(jsonPath("$.startDate[2]").value(bookingRequest.getStartDate().getDayOfMonth()))
                .andExpect(jsonPath("$.endDate[0]").value(bookingRequest.getEndDate().getYear()))
                .andExpect(jsonPath("$.endDate[1]").value(bookingRequest.getEndDate().getMonthValue()))
                .andExpect(jsonPath("$.endDate[2]").value(bookingRequest.getEndDate().getDayOfMonth()))
                .andExpect(jsonPath("$.totalAmount").value(4500))
                .andExpect(jsonPath("$.status").value("CONFIRMED"))
                .andExpect(jsonPath("$.isReviewed").value(false));

        ArgumentCaptor<BookingRequestDTO> requestCaptor = ArgumentCaptor.forClass(BookingRequestDTO.class);
        ArgumentCaptor<String> emailCaptor = ArgumentCaptor.forClass(String.class);
        verify(bookingService, times(1)).createBooking(requestCaptor.capture(), emailCaptor.capture());
        assertNotNull(requestCaptor.getValue());
        assertEquals(100L, requestCaptor.getValue().getVehicleId());
        assertEquals(bookingRequest.getStartDate(), requestCaptor.getValue().getStartDate());
        assertEquals(bookingRequest.getEndDate(), requestCaptor.getValue().getEndDate());
        assertEquals("ashutosh@example.com", emailCaptor.getValue());
        verifyNoMoreInteractions(bookingService);
    }

    @Test
    void createBooking_WhenRequestIsInvalid_ReturnsBadRequest() throws Exception {
        // GIVEN
        BookingRequestDTO invalidRequest = new BookingRequestDTO();
        invalidRequest.setStartDate(LocalDate.now().minusDays(1));

        // WHEN
        mockMvc.perform(post("/api/bookings")
                        .principal(new UsernamePasswordAuthenticationToken("ashutosh@example.com", null))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(invalidRequest)))

                // THEN
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.status").value(400))
                .andExpect(jsonPath("$.errors.vehicleId").value("Vehicle ID is required"))
                .andExpect(jsonPath("$.errors.startDate").value("Start date cannot be in the past"))
                .andExpect(jsonPath("$.errors.endDate").value("End date is required"));

        verify(bookingService, never()).createBooking(any(BookingRequestDTO.class), any(String.class));
    }

    @Test
    void createBooking_WhenServiceThrowsIllegalStateException_ReturnsBadRequest() throws Exception {
        // GIVEN
        UsernamePasswordAuthenticationToken authentication =
                new UsernamePasswordAuthenticationToken("ashutosh@example.com", null);
        when(bookingService.createBooking(any(BookingRequestDTO.class), any(String.class)))
                .thenThrow(new IllegalStateException("Vehicle is already booked during these dates."));

        // WHEN
        mockMvc.perform(post("/api/bookings")
                        .principal(authentication)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(bookingRequest)))

                // THEN
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.status").value(400))
                .andExpect(jsonPath("$.error").value("Vehicle is already booked during these dates."));

        verify(bookingService, times(1)).createBooking(any(BookingRequestDTO.class), any(String.class));
    }

    @Test
    void getMyBookings_WithUserDetailsPrincipal_ReturnsBookingHistory() throws Exception {
        // GIVEN
        UserDetails principal = User.withUsername("details@example.com")
                .password("secret123")
                .roles("USER")
                .build();
        UsernamePasswordAuthenticationToken authentication =
                new UsernamePasswordAuthenticationToken(principal, null, principal.getAuthorities());
        BookingResponseDTO secondBooking = buildBookingResponse(501L, "details@example.com", BookingStatus.ACTIVE, true);
        when(bookingService.getUserBookings("details@example.com"))
                .thenReturn(List.of(
                        buildBookingResponse(500L, "details@example.com", BookingStatus.CONFIRMED, false),
                        secondBooking
                ));

        // WHEN
        mockMvc.perform(get("/api/bookings/my-bookings").principal(authentication))

                // THEN
                .andExpect(status().isOk())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$[0].id").value(500L))
                .andExpect(jsonPath("$[0].userEmail").value("details@example.com"))
                .andExpect(jsonPath("$[0].status").value("CONFIRMED"))
                .andExpect(jsonPath("$[0].isReviewed").value(false))
                .andExpect(jsonPath("$[1].id").value(501L))
                .andExpect(jsonPath("$[1].status").value("ACTIVE"))
                .andExpect(jsonPath("$[1].isReviewed").value(true));

        verify(bookingService, times(1)).getUserBookings("details@example.com");
    }

    @Test
    void cancelBooking_WithStringPrincipal_ReturnsCancelledBooking() throws Exception {
        // GIVEN
        UsernamePasswordAuthenticationToken authentication =
                new UsernamePasswordAuthenticationToken("ashutosh@example.com", null);
        when(bookingService.cancelBooking(500L, "ashutosh@example.com")).thenReturn(cancelledBookingResponse);

        // WHEN
        mockMvc.perform(put("/api/bookings/500/cancel").principal(authentication))

                // THEN
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(500L))
                .andExpect(jsonPath("$.status").value("CANCELLED"))
                .andExpect(jsonPath("$.userEmail").value("ashutosh@example.com"));

        verify(bookingService, times(1)).cancelBooking(500L, "ashutosh@example.com");
    }

    @Test
    void cancelBooking_WhenServiceThrowsSecurityException_ReturnsForbidden() throws Exception {
        // GIVEN
        UsernamePasswordAuthenticationToken authentication =
                new UsernamePasswordAuthenticationToken("intruder@example.com", null);
        when(bookingService.cancelBooking(500L, "intruder@example.com"))
                .thenThrow(new SecurityException("You do not have permission to cancel this booking."));

        // WHEN
        mockMvc.perform(put("/api/bookings/500/cancel").principal(authentication))

                // THEN
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.status").value(403))
                .andExpect(jsonPath("$.error").value("You do not have permission to cancel this booking."));

        verify(bookingService, times(1)).cancelBooking(500L, "intruder@example.com");
    }

    @Test
    void getAllBookingsAdmin_ReturnsAllBookings() throws Exception {
        // GIVEN
        BookingResponseDTO adminBooking = buildBookingResponse(502L, "admin-view@example.com", BookingStatus.COMPLETED, true);
        when(bookingService.getAllBookingsForAdmin()).thenReturn(List.of(bookingResponse, adminBooking));

        // WHEN
        mockMvc.perform(get("/api/bookings/admin/all"))

                // THEN
                .andExpect(status().isOk())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$[0].id").value(500L))
                .andExpect(jsonPath("$[1].id").value(502L))
                .andExpect(jsonPath("$[1].status").value("COMPLETED"))
                .andExpect(jsonPath("$[1].isReviewed").value(true));

        verify(bookingService, times(1)).getAllBookingsForAdmin();
    }

    @Test
    void completeBooking_ReturnsCompletedBooking() throws Exception {
        // GIVEN
        when(bookingService.completeBooking(500L)).thenReturn(completedBookingResponse);

        // WHEN
        mockMvc.perform(put("/api/bookings/admin/500/complete"))

                // THEN
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(500L))
                .andExpect(jsonPath("$.status").value("COMPLETED"))
                .andExpect(jsonPath("$.isReviewed").value(true));

        verify(bookingService, times(1)).completeBooking(500L);
    }

    @Test
    void completeBooking_WhenServiceThrowsResourceNotFoundException_ReturnsNotFound() throws Exception {
        // GIVEN
        when(bookingService.completeBooking(999L)).thenThrow(new ResourceNotFoundException("Booking not found"));

        // WHEN
        mockMvc.perform(put("/api/bookings/admin/999/complete"))

                // THEN
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.status").value(404))
                .andExpect(jsonPath("$.error").value("Booking not found"));

        verify(bookingService, times(1)).completeBooking(999L);
    }

    private BookingResponseDTO buildBookingResponse(Long bookingId, String userEmail, BookingStatus status, boolean isReviewed) {
        return BookingResponseDTO.builder()
                .id(bookingId)
                .userId(1L)
                .userName("Ashutosh Khadse")
                .userEmail(userEmail)
                .vehicleId(100L)
                .vehicleName("Toyota Camry")
                .vehicleType(VehicleType.CAR)
                .vehicleMake("Toyota")
                .vehicleModel("Camry")
                .startDate(LocalDate.now().plusDays(1))
                .endDate(LocalDate.now().plusDays(3))
                .totalAmount(BigDecimal.valueOf(4500))
                .status(status)
                .createdAt(LocalDateTime.of(2026, 5, 1, 12, 30))
                .isReviewed(isReviewed)
                .build();
    }
}
