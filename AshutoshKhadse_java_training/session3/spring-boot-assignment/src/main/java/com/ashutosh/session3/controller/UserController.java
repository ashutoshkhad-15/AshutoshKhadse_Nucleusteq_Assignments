package com.ashutosh.session3.controller;

import com.ashutosh.session3.model.User;
import com.ashutosh.session3.service.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
// Setting this class up as a RestController so Spring knows it will handle incoming HTTP requests
@RestController
public class UserController {

    private final UserService userService;

    // Strict Constructor Injection
    public UserController(UserService userService) {
        this.userService = userService;
    }
}
