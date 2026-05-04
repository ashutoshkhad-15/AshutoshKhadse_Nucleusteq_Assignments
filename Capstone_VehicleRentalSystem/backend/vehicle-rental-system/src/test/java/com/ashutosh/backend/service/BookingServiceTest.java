package com.ashutosh.backend.service;

import com.ashutosh.backend.dto.request.BookingRequestDTO;
import com.ashutosh.backend.dto.response.BookingResponseDTO;
import com.ashutosh.backend.entity.AppUser;
import com.ashutosh.backend.entity.Booking;
import com.ashutosh.backend.entity.Vehicle;
import com.ashutosh.backend.enums.BookingStatus;
import com.ashutosh.backend.enums.UserRole;
import com.ashutosh.backend.enums.VehicleStatus;
import com.ashutosh.backend.enums.VehicleType;
import com.ashutosh.backend.repository.AppUserRepository;
import com.ashutosh.backend.repository.BookingRepository;
import com.ashutosh.backend.repository.ReviewRepository;
import com.ashutosh.backend.repository.VehicleRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

/**
 * Unit tests for the BookingService class.
 * Tests complex business logic including date constraints, overlap detection,
 * role-based cancellation permissions, and automatic state transitions.
 */
@ExtendWith(MockitoExtension.class)
class BookingServiceTest {

    @Mock
    private BookingRepository bookingRepository;
    @Mock
    private VehicleRepository vehicleRepository;
    @Mock
    private AppUserRepository appuserRepository;
    @Mock
    private ReviewRepository reviewRepository;

    @InjectMocks
    private BookingService bookingService;

    private AppUser mockUser;
    private AppUser mockAdmin;
    private Vehicle mockVehicle;
    private Booking mockBooking;
    private BookingRequestDTO requestDTO;

    @BeforeEach
    void setUp() {
        // Setup User
        mockUser = AppUser.builder()
                .id(1L)
                .firstName("John")
                .lastName("Doe")
                .email("user@example.com")
                .role(UserRole.USER)
                .build();

        // Setup Admin
        mockAdmin = AppUser.builder()
                .id(2L)
                .firstName("Admin")
                .lastName("User")
                .email("admin@example.com")
                .role(UserRole.ADMIN)
                .build();

        // Setup Vehicle
        mockVehicle = Vehicle.builder()
                .id(100L)
                .make("Toyota")
                .model("Camry")
                .vehicleType(VehicleType.CAR)
                .dailyRate(BigDecimal.valueOf(1000))
                .status(VehicleStatus.AVAILABLE)
                .build();

        // Setup Booking Request (Valid: Starts tomorrow, ends in 3 days)
        requestDTO = new BookingRequestDTO();
        requestDTO.setVehicleId(100L);
        requestDTO.setStartDate(LocalDate.now().plusDays(1));
        requestDTO.setEndDate(LocalDate.now().plusDays(3));

        // Setup Saved Booking Entity
        mockBooking = Booking.builder()
                .id(500L)
                .user(mockUser)
                .vehicle(mockVehicle)
                .startDate(LocalDate.now().plusDays(1))
                .endDate(LocalDate.now().plusDays(3))
                .pricePerDay(BigDecimal.valueOf(1000))
                .totalAmount(BigDecimal.valueOf(3000))
                .status(BookingStatus.CONFIRMED)
                .createdAt(LocalDateTime.now())
                .build();
    }

    // 1. CREATE BOOKING TESTS
    @Test
    void createBooking_Success() {
        // GIVEN
        when(appuserRepository.findByEmail("user@example.com")).thenReturn(Optional.of(mockUser));
        when(vehicleRepository.findById(100L)).thenReturn(Optional.of(mockVehicle));
        when(bookingRepository.findConflictingBookings(eq(100L), any(LocalDate.class), any(LocalDate.class)))
                .thenReturn(new ArrayList<>()); // No conflicts
        when(bookingRepository.save(any(Booking.class))).thenReturn(mockBooking);
        lenient().when(reviewRepository.existsByBookingId(500L)).thenReturn(false);

        // WHEN
        BookingResponseDTO response = bookingService.createBooking(requestDTO, "user@example.com");

        // THEN
        assertNotNull(response);
        assertEquals(BookingStatus.CONFIRMED, response.getStatus());
        assertEquals(BigDecimal.valueOf(3000), response.getTotalAmount());
        verify(bookingRepository, times(1)).save(any(Booking.class));
    }

    @Test
    void createBooking_EndBeforeStart_ThrowsException() {
        // GIVEN
        requestDTO.setStartDate(LocalDate.now().plusDays(3));
        requestDTO.setEndDate(LocalDate.now().plusDays(1)); // Invalid

        // WHEN & THEN
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                () -> bookingService.createBooking(requestDTO, "user@example.com"));
        assertTrue(ex.getMessage().contains("before start date"));
    }

    @Test
    void createBooking_DurationExceeds30Days_ThrowsException() {
        // GIVEN
        requestDTO.setStartDate(LocalDate.now().plusDays(1));
        requestDTO.setEndDate(LocalDate.now().plusDays(35)); // > 30 days

        // WHEN & THEN
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                () -> bookingService.createBooking(requestDTO, "user@example.com"));
        assertTrue(ex.getMessage().contains("exceed 30 days"));
    }

    @Test
    void createBooking_VehicleNotAvailable_ThrowsException() {
        // GIVEN
        mockVehicle.setStatus(VehicleStatus.MAINTENANCE); // Not available
        when(appuserRepository.findByEmail("user@example.com")).thenReturn(Optional.of(mockUser));
        when(vehicleRepository.findById(100L)).thenReturn(Optional.of(mockVehicle));

        // WHEN & THEN
        IllegalStateException ex = assertThrows(IllegalStateException.class,
                () -> bookingService.createBooking(requestDTO, "user@example.com"));
        assertTrue(ex.getMessage().contains("no longer available"));
    }

    @Test
    void createBooking_DateConflictExists_ThrowsException() {
        // GIVEN
        when(appuserRepository.findByEmail("user@example.com")).thenReturn(Optional.of(mockUser));
        when(vehicleRepository.findById(100L)).thenReturn(Optional.of(mockVehicle));
        // Simulate an existing conflicting booking
        when(bookingRepository.findConflictingBookings(eq(100L), any(LocalDate.class), any(LocalDate.class)))
                .thenReturn(List.of(new Booking()));

        // WHEN & THEN
        IllegalStateException ex = assertThrows(IllegalStateException.class,
                () -> bookingService.createBooking(requestDTO, "user@example.com"));
        assertTrue(ex.getMessage().contains("already booked"));
    }

    // 2. CANCELLATION TESTS
    @Test
    void cancelBooking_Success_ByUser() {
        // GIVEN: Future booking owned by the user
        when(bookingRepository.findById(500L)).thenReturn(Optional.of(mockBooking));
        when(appuserRepository.findByEmail("user@example.com")).thenReturn(Optional.of(mockUser));
        when(bookingRepository.save(any(Booking.class))).thenReturn(mockBooking);
        lenient().when(reviewRepository.existsByBookingId(500L)).thenReturn(false);

        // WHEN
        BookingResponseDTO response = bookingService.cancelBooking(500L, "user@example.com");

        // THEN
        assertEquals(BookingStatus.CANCELLED, mockBooking.getStatus());
        verify(bookingRepository, times(1)).save(mockBooking);
    }

    @Test
    void cancelBooking_Success_ByAdmin() {
        // GIVEN: Future booking owned by user, but Admin requests cancellation
        when(bookingRepository.findById(500L)).thenReturn(Optional.of(mockBooking));
        when(appuserRepository.findByEmail("admin@example.com")).thenReturn(Optional.of(mockAdmin));
        when(bookingRepository.save(any(Booking.class))).thenReturn(mockBooking);
        lenient().when(reviewRepository.existsByBookingId(500L)).thenReturn(false);

        // WHEN
        bookingService.cancelBooking(500L, "admin@example.com");

        // THEN
        assertEquals(BookingStatus.CANCELLED, mockBooking.getStatus());
    }

    @Test
    void cancelBooking_UnauthorizedUser_ThrowsException() {
        // GIVEN: Booking owned by mockUser, but a different regular user tries to cancel
        AppUser sneakyUser = AppUser.builder().id(99L).email("sneaky@example.com").role(UserRole.USER).build();
        when(bookingRepository.findById(500L)).thenReturn(Optional.of(mockBooking));
        when(appuserRepository.findByEmail("sneaky@example.com")).thenReturn(Optional.of(sneakyUser));

        // WHEN & THEN
        assertThrows(SecurityException.class, () -> bookingService.cancelBooking(500L, "sneaky@example.com"));
    }

    @Test
    void cancelBooking_AlreadyActive_ThrowsException() {
        // GIVEN: Booking is currently active
        mockBooking.setStatus(BookingStatus.ACTIVE);
        when(bookingRepository.findById(500L)).thenReturn(Optional.of(mockBooking));
        when(appuserRepository.findByEmail("user@example.com")).thenReturn(Optional.of(mockUser));

        // WHEN & THEN
        IllegalStateException ex = assertThrows(IllegalStateException.class, () -> bookingService.cancelBooking(500L, "user@example.com"));
        assertTrue(ex.getMessage().contains("ongoing booking"));
    }

    @Test
    void cancelBooking_StartDateIsToday_ThrowsException() {
        // GIVEN: Booking starts today
        mockBooking.setStartDate(LocalDate.now());
        when(bookingRepository.findById(500L)).thenReturn(Optional.of(mockBooking));
        when(appuserRepository.findByEmail("user@example.com")).thenReturn(Optional.of(mockUser));

        // WHEN & THEN
        IllegalStateException ex = assertThrows(IllegalStateException.class, () -> bookingService.cancelBooking(500L, "user@example.com"));
        assertTrue(ex.getMessage().contains("on or after the start date"));
    }

    // 3. COMPLETE BOOKING TESTS
    @Test
    void completeBooking_Success() {
        // GIVEN
        mockBooking.setStatus(BookingStatus.ACTIVE);
        when(bookingRepository.findById(500L)).thenReturn(Optional.of(mockBooking));
        when(bookingRepository.save(any(Booking.class))).thenReturn(mockBooking);
        lenient().when(reviewRepository.existsByBookingId(500L)).thenReturn(false);

        // WHEN
        BookingResponseDTO response = bookingService.completeBooking(500L);

        // THEN
        assertEquals(BookingStatus.COMPLETED, response.getStatus());
        verify(bookingRepository, times(1)).save(mockBooking);
    }

    // 4. GET BOOKINGS & EVALUATION LOGIC TESTS
    @Test
    void getUserBookings_TriggersEvaluation_ToActive() {
        // GIVEN: A booking that is CONFIRMED, but its start date is today
        mockBooking.setStartDate(LocalDate.now());
        mockBooking.setEndDate(LocalDate.now().plusDays(2));
        mockBooking.setStatus(BookingStatus.CONFIRMED);

        when(appuserRepository.findByEmail("user@example.com")).thenReturn(Optional.of(mockUser));
        when(bookingRepository.findByUser_IdOrderByCreatedAtDesc(1L)).thenReturn(List.of(mockBooking));
        lenient().when(reviewRepository.existsByBookingId(500L)).thenReturn(false);

        // WHEN
        List<BookingResponseDTO> responses = bookingService.getUserBookings("user@example.com");

        // THEN: The private evaluateBookings method should have upgraded the status to ACTIVE
        assertEquals(1, responses.size());
        assertEquals(BookingStatus.ACTIVE, responses.get(0).getStatus());
        verify(bookingRepository, times(1)).saveAll(anyList()); // Verifies the DB was updated
    }
}