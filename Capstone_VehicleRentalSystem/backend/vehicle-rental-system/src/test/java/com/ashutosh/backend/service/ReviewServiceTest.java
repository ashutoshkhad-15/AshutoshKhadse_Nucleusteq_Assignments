package com.ashutosh.backend.service;

import com.ashutosh.backend.dto.request.ReviewRequestDTO;
import com.ashutosh.backend.dto.response.ReviewResponseDTO;
import com.ashutosh.backend.entity.AppUser;
import com.ashutosh.backend.entity.Booking;
import com.ashutosh.backend.entity.Review;
import com.ashutosh.backend.entity.Vehicle;
import com.ashutosh.backend.enums.BookingStatus;
import com.ashutosh.backend.enums.UserRole;
import com.ashutosh.backend.exception.DuplicateResourceException;
import com.ashutosh.backend.exception.ResourceNotFoundException;
import com.ashutosh.backend.repository.AppUserRepository;
import com.ashutosh.backend.repository.BookingRepository;
import com.ashutosh.backend.repository.ReviewRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class ReviewServiceTest {

    @Mock
    private ReviewRepository reviewRepository;

    @Mock
    private BookingRepository bookingRepository;

    @Mock
    private AppUserRepository appuserRepository;

    @InjectMocks
    private ReviewService reviewService;

    private AppUser author;
    private AppUser admin;
    private AppUser anotherUser;
    private Vehicle vehicle;
    private Booking completedBooking;
    private ReviewRequestDTO reviewRequest;
    private Review savedReview;

    @BeforeEach
    void setUp() {
        author = AppUser.builder()
                .id(1L)
                .firstName("Ashutosh")
                .lastName("Khadse")
                .email("ashutosh@example.com")
                .role(UserRole.USER)
                .build();

        admin = AppUser.builder()
                .id(2L)
                .firstName("Admin")
                .lastName("User")
                .email("admin@example.com")
                .role(UserRole.ADMIN)
                .build();

        anotherUser = AppUser.builder()
                .id(3L)
                .firstName("Sneaky")
                .lastName("User")
                .email("sneaky@example.com")
                .role(UserRole.USER)
                .build();

        vehicle = Vehicle.builder()
                .id(100L)
                .make("Toyota")
                .model("Camry")
                .build();

        completedBooking = Booking.builder()
                .id(10L)
                .user(author)
                .vehicle(vehicle)
                .status(BookingStatus.COMPLETED)
                .build();

        reviewRequest = new ReviewRequestDTO();
        reviewRequest.setBookingId(10L);
        reviewRequest.setRating(5);
        reviewRequest.setComment("Excellent ride quality and service.");

        savedReview = Review.builder()
                .id(20L)
                .booking(completedBooking)
                .rating(5)
                .comment("Excellent ride quality and service.")
                .createdAt(LocalDateTime.of(2026, 4, 30, 10, 15))
                .build();
    }

    @Test
    void addReview_Success() {
        // GIVEN
        when(bookingRepository.findById(10L)).thenReturn(Optional.of(completedBooking));
        when(reviewRepository.existsByBookingId(10L)).thenReturn(false);
        when(reviewRepository.save(any(Review.class))).thenReturn(savedReview);

        // WHEN
        ReviewResponseDTO response = reviewService.addReview(reviewRequest, "ashutosh@example.com");

        // THEN
        ArgumentCaptor<Review> reviewCaptor = ArgumentCaptor.forClass(Review.class);
        verify(reviewRepository, times(1)).save(reviewCaptor.capture());
        Review persistedReview = reviewCaptor.getValue();

        assertNotNull(response);
        assertEquals(20L, response.getId());
        assertEquals(10L, response.getBookingId());
        assertEquals(5, response.getRating());
        assertEquals("Excellent ride quality and service.", response.getComment());
        assertEquals("Ashutosh", response.getReviewerFirstName());
        assertEquals("ashutosh@example.com", response.getReviewerEmail());
        assertEquals(savedReview.getCreatedAt(), response.getCreatedAt());
        assertEquals(completedBooking, persistedReview.getBooking());
        assertEquals(5, persistedReview.getRating());
        assertEquals("Excellent ride quality and service.", persistedReview.getComment());
    }

    @Test
    void addReview_BookingNotFound_ThrowsException() {
        // GIVEN
        when(bookingRepository.findById(10L)).thenReturn(Optional.empty());

        // WHEN
        ResourceNotFoundException exception = assertThrows(ResourceNotFoundException.class,
                () -> reviewService.addReview(reviewRequest, "ashutosh@example.com"));

        // THEN
        assertEquals("Booking not found", exception.getMessage());
        verify(reviewRepository, never()).save(any(Review.class));
    }

    @Test
    void addReview_WhenUserDoesNotOwnBooking_ThrowsSecurityException() {
        // GIVEN
        when(bookingRepository.findById(10L)).thenReturn(Optional.of(completedBooking));

        // WHEN
        SecurityException exception = assertThrows(SecurityException.class,
                () -> reviewService.addReview(reviewRequest, "sneaky@example.com"));

        // THEN
        assertEquals("You can only review your own bookings.", exception.getMessage());
        verify(reviewRepository, never()).existsByBookingId(any());
        verify(reviewRepository, never()).save(any(Review.class));
    }

    @Test
    void addReview_WhenBookingIsNotCompleted_ThrowsIllegalStateException() {
        // GIVEN
        completedBooking.setStatus(BookingStatus.ACTIVE);
        when(bookingRepository.findById(10L)).thenReturn(Optional.of(completedBooking));

        // WHEN
        IllegalStateException exception = assertThrows(IllegalStateException.class,
                () -> reviewService.addReview(reviewRequest, "ashutosh@example.com"));

        // THEN
        assertEquals("Reviews can only be submitted for completed trips.", exception.getMessage());
        verify(reviewRepository, never()).existsByBookingId(any());
        verify(reviewRepository, never()).save(any(Review.class));
    }

    @Test
    void addReview_WhenReviewAlreadyExists_ThrowsDuplicateResourceException() {
        // GIVEN
        when(bookingRepository.findById(10L)).thenReturn(Optional.of(completedBooking));
        when(reviewRepository.existsByBookingId(10L)).thenReturn(true);

        // WHEN
        DuplicateResourceException exception = assertThrows(DuplicateResourceException.class,
                () -> reviewService.addReview(reviewRequest, "ashutosh@example.com"));

        // THEN
        assertEquals("A review has already been submitted for this booking.", exception.getMessage());
        verify(reviewRepository, never()).save(any(Review.class));
    }

    @Test
    void getVehicleReviews_ReturnsMappedReviewResponses() {
        // GIVEN
        Review olderReview = Review.builder()
                .id(21L)
                .booking(completedBooking)
                .rating(4)
                .comment("Comfortable and smooth.")
                .createdAt(LocalDateTime.of(2026, 4, 29, 8, 0))
                .build();
        when(reviewRepository.findByBooking_Vehicle_IdOrderByCreatedAtDesc(100L))
                .thenReturn(List.of(savedReview, olderReview));

        // WHEN
        List<ReviewResponseDTO> responses = reviewService.getVehicleReviews(100L);

        // THEN
        assertEquals(2, responses.size());
        assertEquals(20L, responses.get(0).getId());
        assertEquals(5, responses.get(0).getRating());
        assertEquals("Excellent ride quality and service.", responses.get(0).getComment());
        assertEquals("Ashutosh", responses.get(0).getReviewerFirstName());
        assertEquals("ashutosh@example.com", responses.get(0).getReviewerEmail());
        assertEquals(21L, responses.get(1).getId());
        assertEquals(4, responses.get(1).getRating());
        assertEquals("Comfortable and smooth.", responses.get(1).getComment());
    }

    @Test
    void deleteReview_Success_ByAuthor() {
        // GIVEN
        when(reviewRepository.findById(20L)).thenReturn(Optional.of(savedReview));
        when(appuserRepository.findByEmail("ashutosh@example.com")).thenReturn(Optional.of(author));

        // WHEN
        reviewService.deleteReview(20L, "ashutosh@example.com");

        // THEN
        verify(reviewRepository, times(1)).delete(savedReview);
    }

    @Test
    void deleteReview_Success_ByAdmin() {
        // GIVEN
        when(reviewRepository.findById(20L)).thenReturn(Optional.of(savedReview));
        when(appuserRepository.findByEmail("admin@example.com")).thenReturn(Optional.of(admin));

        // WHEN
        reviewService.deleteReview(20L, "admin@example.com");

        // THEN
        verify(reviewRepository, times(1)).delete(savedReview);
    }

    @Test
    void deleteReview_ReviewNotFound_ThrowsException() {
        // GIVEN
        when(reviewRepository.findById(99L)).thenReturn(Optional.empty());

        // WHEN
        ResourceNotFoundException exception = assertThrows(ResourceNotFoundException.class,
                () -> reviewService.deleteReview(99L, "ashutosh@example.com"));

        // THEN
        assertEquals("Review not found with ID: 99", exception.getMessage());
        verify(appuserRepository, never()).findByEmail("ashutosh@example.com");
        verify(reviewRepository, never()).delete(any(Review.class));
    }

    @Test
    void deleteReview_UserNotFound_ThrowsException() {
        // GIVEN
        when(reviewRepository.findById(20L)).thenReturn(Optional.of(savedReview));
        when(appuserRepository.findByEmail("missing@example.com")).thenReturn(Optional.empty());

        // WHEN
        ResourceNotFoundException exception = assertThrows(ResourceNotFoundException.class,
                () -> reviewService.deleteReview(20L, "missing@example.com"));

        // THEN
        assertEquals("User not found", exception.getMessage());
        verify(reviewRepository, never()).delete(any(Review.class));
    }

    @Test
    void deleteReview_WhenUserIsNeitherAuthorNorAdmin_ThrowsSecurityException() {
        // GIVEN
        when(reviewRepository.findById(20L)).thenReturn(Optional.of(savedReview));
        when(appuserRepository.findByEmail("sneaky@example.com")).thenReturn(Optional.of(anotherUser));

        // WHEN
        SecurityException exception = assertThrows(SecurityException.class,
                () -> reviewService.deleteReview(20L, "sneaky@example.com"));

        // THEN
        assertTrue(exception.getMessage().contains("do not have permission"));
        verify(reviewRepository, never()).delete(any(Review.class));
    }
}
