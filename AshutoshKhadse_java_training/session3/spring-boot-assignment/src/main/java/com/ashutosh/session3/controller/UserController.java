package com.ashutosh.session3.controller;

import com.ashutosh.session3.model.User;
import com.ashutosh.session3.service.UserService;
import com.ashutosh.session3.exception.UserNotFoundException;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.HttpStatus;

import java.util.Map;
import java.util.List;

// Setting this class up as a RestController so Spring knows it will handle incoming HTTP requests
@RestController
// I added @RequestMapping here at the class level to keep things clean.
// Now, all endpoints in this controller will automatically start with "/users"
@RequestMapping("/users")
public class UserController {

    private final UserService userService;

    // Strict Constructor Injection
    public UserController(UserService userService) {
        this.userService = userService;
    }

    // 1. Search API
    // This endpoint will now map to "/users/search" because of the class-level
    // mapping above.
    @GetMapping("/search")
    public ResponseEntity<List<User>> searchUsers(
            // By setting required = false, the client doesn't HAVE to provide these query
            // parameters.
            // If they skip one, Spring just passes 'null' to my variables, which works
            // perfectly
            // with the null-checking logic I wrote earlier in the UserService
            @RequestParam(required = false) String name,
            @RequestParam(required = false) Integer age,
            @RequestParam(required = false) String role) {

        // Passing whatever filters the user provided directly into our service logic
        List<User> results = userService.searchUsers(name, age, role);
        // Sending back the filtered list with a 200 OK status
        return ResponseEntity.ok(results);
    }

    // 2. Submit API
    // I mapped this to "/submit" for POST requests (so the full URL is POST /users/submit).
    // I used POST to save new data.
    @PostMapping("/submit")
    public ResponseEntity<Map<String, String>> submitData(
            // @RequestBody automatically takes the JSON string the user sent and converts it into our Java User object.
            // I added 'required = false' here This way, if someone sends a completely empty POST request,
            // my Service layer's validateUser() method can catch the 'null' and return custom error message
            // instead of Spring throwing a generic missing body error before it even reaches code
            @RequestBody(required = false) User user) {

            // Calling the service method to validate and save the user
            userService.saveUser(user);

            // I'm putting the response inside Map.of() so it gets sent back as proper, clean JSON
            // instead of just a raw text string.
            return ResponseEntity.status(HttpStatus.CREATED)
                    .body(Map.of("message", "User successfully created"));
    }

    // 3. Delete API
    @DeleteMapping("/{id}")
    public ResponseEntity<Map<String, String>> deleteUser(
            // Grabbing the ID straight from the URL path
            @PathVariable Long id,
            // Adding a safety check If they don't pass '?confirm=true' in the URL,
            // the service layer will block the deletion.
            @RequestParam(required = false) Boolean confirm) {

            // Handing it off to the service layer to do the actual deleting
            userService.deleteUser(id, confirm);

            // If no exceptions were thrown, it was a success
            // Sending back a 200 OK with a clean JSON message.
            return ResponseEntity.ok(
                    Map.of("message", "User deleted successfully")
            );
    }
}
