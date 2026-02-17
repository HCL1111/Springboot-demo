package com.example.demo.controller;

import com.example.demo.entity.User;
import com.example.demo.service.UserService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

@RestController
@RequestMapping("/api/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping
    public ResponseEntity<List<User>> getAllUsers() {
        List<User> users = userService.getAllUsers();
        return ResponseEntity.ok(users);
    }

    @GetMapping("/{id}")
    public ResponseEntity<User> getUserById(@PathVariable Long id) {
        return userService.getUserById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/email/{email}")
    public ResponseEntity<User> getUserByEmail(@PathVariable String email) {
        return userService.getUserByEmail(email)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody User user) {
        try {
            User createdUser = userService.createUser(user);
            return ResponseEntity.status(HttpStatus.CREATED).body(createdUser);
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().build();
        }
    }

    @PutMapping("/{id}")
    public ResponseEntity<User> updateUser(@PathVariable Long id, @RequestBody User userDetails) {
        try {
            User updatedUser = userService.updateUser(id, userDetails);
            return ResponseEntity.ok(updatedUser);
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        try {
            userService.deleteUser(id);
            return ResponseEntity.noContent().build();
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }

    // VULNERABILITY: Path Traversal - allows reading arbitrary files
    @GetMapping("/file/{filename}")
    public ResponseEntity<String> readFile(@PathVariable String filename) {
        try {
            // Vulnerable: No path validation - allows "../../../etc/passwd" type attacks
            String content = new String(Files.readAllBytes(Paths.get("/app/data/" + filename)));
            return ResponseEntity.ok(content);
        } catch (IOException e) {
            return ResponseEntity.notFound().build();
        }
    }

    // VULNERABILITY: SQL Injection - search users by name
    @GetMapping("/search")
    public ResponseEntity<List<User>> searchUsersByName(@RequestParam String name) {
        // Vulnerable: Direct string concatenation in SQL query
        List<User> users = userService.searchUsersByName(name);
        return ResponseEntity.ok(users);
    }

    // VULNERABILITY: Command Injection - execute system commands
    @GetMapping("/ping")
    public ResponseEntity<String> pingHost(@RequestParam String host) {
        try {
            // Vulnerable: Executing shell command with user input
            Process process = Runtime.getRuntime().exec("ping -c 1 " + host);
            return ResponseEntity.ok("Ping executed for: " + host);
        } catch (IOException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error: " + e.getMessage());
        }
    }

}
