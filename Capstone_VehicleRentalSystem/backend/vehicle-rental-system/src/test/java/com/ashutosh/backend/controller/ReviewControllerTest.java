package com.ashutosh.backend.controller;

import com.ashutosh.backend.dto.request.ReviewRequestDTO;
import com.ashutosh.backend.dto.response.ReviewResponseDTO;
import com.ashutosh.backend.entity.AppUser;
import com.ashutosh.backend.enums.UserRole;
import com.ashutosh.backend.exception.DuplicateResourceException;
import com.ashutosh.backend.exception.GlobalExceptionHandler;
import com.ashutosh.backend.exception.ResourceNotFoundException;
import com.ashutosh.backend.service.ReviewService;
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

import java.time.LocalDateTime;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoMoreInteractions;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@ExtendWith(MockitoExtension.class)
class ReviewControllerTest {

    @Mock
    private ReviewService reviewService;

    @InjectMocks
    private ReviewController reviewController;

    private MockMvc mockMvc;
    private ObjectMapper objectMapper;
    private ReviewRequestDTO reviewRequest;
    private ReviewResponseDTO reviewResponse;

    @BeforeEach
    void setUp() {
        LocalValidatorFactoryBean validator = new LocalValidatorFactoryBean();
        validator.afterPropertiesSet();

        mockMvc = MockMvcBuilders.standaloneSetup(reviewController)
                .setControllerAdvice(new GlobalExceptionHandler())
                .setValidator(validator)
                .build();

        objectMapper = new ObjectMapper().findAndRegisterModules();

        reviewRequest = new ReviewRequestDTO();
        reviewRequest.setBookingId(10L);
        reviewRequest.setRating(5);
        reviewRequest.setComment("Excellent ride quality and service.");

        reviewResponse = ReviewResponseDTO.builder()
                .id(20L)
                .bookingId(10L)
                .rating(5)
                .comment("Excellent ride quality and service.")
                .reviewerFirstName("Ashutosh")
                .reviewerEmail("ashutosh@example.com")
                .createdAt(LocalDateTime.of(2026, 5, 1, 12, 40))
                .build();
    }

    @Test
    void addReview_ReturnsCreatedReview() throws Exception {
        // GIVEN
        AppUser principal = AppUser.builder()
                .id(1L)
                .email("ashutosh@example.com")
                .role(UserRole.USER)
                .build();
        UsernamePasswordAuthenticationToken authentication =
                new UsernamePasswordAuthenticationToken(principal, null);
        when(reviewService.addReview(any(ReviewRequestDTO.class), any(String.class))).thenReturn(reviewResponse);

        // WHEN
        mockMvc.perform(post("/api/reviews")
                        .principal(authentication)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(reviewRequest)))

                // THEN
                .andExpect(status().isCreated())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$.id").value(20L))
                .andExpect(jsonPath("$.bookingId").value(10L))
                .andExpect(jsonPath("$.rating").value(5))
                .andExpect(jsonPath("$.comment").value("Excellent ride quality and service."))
                .andExpect(jsonPath("$.reviewerFirstName").value("Ashutosh"))
                .andExpect(jsonPath("$.reviewerEmail").value("ashutosh@example.com"));

        ArgumentCaptor<ReviewRequestDTO> requestCaptor = ArgumentCaptor.forClass(ReviewRequestDTO.class);
        ArgumentCaptor<String> emailCaptor = ArgumentCaptor.forClass(String.class);
        verify(reviewService, times(1)).addReview(requestCaptor.capture(), emailCaptor.capture());
        assertNotNull(requestCaptor.getValue());
        assertEquals(10L, requestCaptor.getValue().getBookingId());
        assertEquals(5, requestCaptor.getValue().getRating());
        assertEquals("Excellent ride quality and service.", requestCaptor.getValue().getComment());
        assertEquals("ashutosh@example.com", emailCaptor.getValue());
        verifyNoMoreInteractions(reviewService);
    }

    @Test
    void addReview_WhenRequestIsInvalid_ReturnsBadRequest() throws Exception {
        // GIVEN
        ReviewRequestDTO invalidRequest = new ReviewRequestDTO();
        invalidRequest.setRating(0);

        // WHEN
        mockMvc.perform(post("/api/reviews")
                        .principal(new UsernamePasswordAuthenticationToken("ashutosh@example.com", null))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(invalidRequest)))

                // THEN
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.status").value(400))
                .andExpect(jsonPath("$.errors.bookingId").value("Booking ID is required"))
                .andExpect(jsonPath("$.errors.rating").value("Rating must be at least 1"));

        verify(reviewService, never()).addReview(any(ReviewRequestDTO.class), any(String.class));
    }

    @Test
    void addReview_WhenServiceThrowsDuplicateResourceException_ReturnsConflict() throws Exception {
        // GIVEN
        UsernamePasswordAuthenticationToken authentication =
                new UsernamePasswordAuthenticationToken("ashutosh@example.com", null);
        when(reviewService.addReview(any(ReviewRequestDTO.class), any(String.class)))
                .thenThrow(new DuplicateResourceException("A review has already been submitted for this booking."));

        // WHEN
        mockMvc.perform(post("/api/reviews")
                        .principal(authentication)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(reviewRequest)))

                // THEN
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.status").value(409))
                .andExpect(jsonPath("$.error").value("A review has already been submitted for this booking."));

        verify(reviewService, times(1)).addReview(any(ReviewRequestDTO.class), any(String.class));
    }

    @Test
    void getVehicleReviews_ReturnsVehicleReviewList() throws Exception {
        // GIVEN
        ReviewResponseDTO olderReview = ReviewResponseDTO.builder()
                .id(21L)
                .bookingId(11L)
                .rating(4)
                .comment("Comfortable and smooth.")
                .reviewerFirstName("John")
                .reviewerEmail("john@example.com")
                .createdAt(LocalDateTime.of(2026, 4, 30, 18, 0))
                .build();
        when(reviewService.getVehicleReviews(100L)).thenReturn(List.of(reviewResponse, olderReview));

        // WHEN
        mockMvc.perform(get("/api/reviews/vehicle/100"))

                // THEN
                .andExpect(status().isOk())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$[0].id").value(20L))
                .andExpect(jsonPath("$[0].rating").value(5))
                .andExpect(jsonPath("$[0].reviewerEmail").value("ashutosh@example.com"))
                .andExpect(jsonPath("$[1].id").value(21L))
                .andExpect(jsonPath("$[1].rating").value(4))
                .andExpect(jsonPath("$[1].reviewerFirstName").value("John"));

        verify(reviewService, times(1)).getVehicleReviews(100L);
    }

    @Test
    void deleteReview_WithUserDetailsPrincipal_ReturnsNoContent() throws Exception {
        // GIVEN
        UserDetails principal = User.withUsername("details@example.com")
                .password("secret123")
                .roles("USER")
                .build();
        UsernamePasswordAuthenticationToken authentication =
                new UsernamePasswordAuthenticationToken(principal, null, principal.getAuthorities());

        // WHEN
        mockMvc.perform(delete("/api/reviews/20").principal(authentication))

                // THEN
                .andExpect(status().isNoContent());

        verify(reviewService, times(1)).deleteReview(20L, "details@example.com");
    }

    @Test
    void deleteReview_WithStringPrincipalAndForbiddenResponse() throws Exception {
        // GIVEN
        UsernamePasswordAuthenticationToken authentication =
                new UsernamePasswordAuthenticationToken("intruder@example.com", null);
        doThrow(new SecurityException("You do not have permission to delete this review."))
                .when(reviewService).deleteReview(20L, "intruder@example.com");

        // WHEN
        mockMvc.perform(delete("/api/reviews/20").principal(authentication))

                // THEN
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.status").value(403))
                .andExpect(jsonPath("$.error").value("You do not have permission to delete this review."));

        verify(reviewService, times(1)).deleteReview(20L, "intruder@example.com");
    }

    @Test
    void deleteReview_WhenServiceThrowsNotFound_ReturnsNotFound() throws Exception {
        // GIVEN
        UsernamePasswordAuthenticationToken authentication =
                new UsernamePasswordAuthenticationToken("ashutosh@example.com", null);
        doThrow(new ResourceNotFoundException("Review not found with ID: 99"))
                .when(reviewService).deleteReview(99L, "ashutosh@example.com");

        // WHEN
        mockMvc.perform(delete("/api/reviews/99").principal(authentication))

                // THEN
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.status").value(404))
                .andExpect(jsonPath("$.error").value("Review not found with ID: 99"));

        verify(reviewService, times(1)).deleteReview(99L, "ashutosh@example.com");
    }
}
