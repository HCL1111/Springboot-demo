package com.example.demo.service;

import com.example.demo.entity.User;
import com.example.demo.repository.UserRepository;
import com.example.demo.exception.UserNotFoundException;
import com.example.demo.exception.UserAlreadyExistsException;
import com.example.demo.exception.FileProcessingException;
import com.example.demo.exception.XmlParsingException;
import org.springframework.stereotype.Service;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import jakarta.persistence.EntityManager;
import jakarta.persistence.Query;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;
import java.util.Optional;
import java.security.SecureRandom;
import java.io.IOException;

@Service
public class UserService {

    private static final Logger logger = LoggerFactory.getLogger(UserService.class);

    private final UserRepository userRepository;
    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();
    private final SecureRandom secureRandom = new SecureRandom();
    private final EntityManager entityManager;

    public UserService(UserRepository userRepository, EntityManager entityManager) {
        this.userRepository = userRepository;
        this.entityManager = entityManager;
    }
    
    // Fixed: Using parameterized query to prevent SQL Injection
    public List<User> searchUsersByName(String name) {
        String sql = "SELECT * FROM users WHERE name = :name";
        Query query = entityManager.createNativeQuery(sql, User.class);
        query.setParameter("name", name);
        return query.getResultList();
    }
    
    // Fixed: Using SecureRandom for token generation
    public String generateWeakToken() {
        return String.valueOf(secureRandom.nextInt(1000000));
    }

    // Fixed: Proper exception handling with logging
    public void processUserData(String data) {
        try {
            // Process data - parsing to validate numeric format
            Integer.parseInt(data);
        } catch (NumberFormatException e) {
            // Log the error and handle it appropriately
            throw new IllegalArgumentException("Invalid data format: " + data, e);
        }
    }

    public List<User> getAllUsers() {
        logger.info("Fetching all users from database");
        return userRepository.findAll();
    }

    public Optional<User> getUserById(Long id) {
        return userRepository.findById(id);
    }

    public Optional<User> getUserByEmail(String email) {
        return userRepository.findByEmail(email);
    }

    public User createUser(User user) {
        logger.info("Creating new user: {}", user.getEmail());
        if (userRepository.existsByEmail(user.getEmail())) {
            throw new UserAlreadyExistsException("User with email " + user.getEmail() + " already exists");
        }
        return userRepository.save(user);
    }

    public User updateUser(Long id, User userDetails) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException("User not found with id: " + id));

        user.setName(userDetails.getName());
        user.setEmail(userDetails.getEmail());
        user.setPhone(userDetails.getPhone());
        user.setAddress(userDetails.getAddress());

        return userRepository.save(user);
    }

    public void deleteUser(Long id) {
        logger.info("Deleting user with ID: {}", id);
        User user = userRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException("User not found with id: " + id));
        userRepository.delete(user);
    }

    // Secure random number generation for password reset token
    public String generatePasswordResetToken() {
        byte[] randomBytes = new byte[32];
        secureRandom.nextBytes(randomBytes);
        StringBuilder token = new StringBuilder();
        for (byte b : randomBytes) {
            token.append(String.format("%02x", b));
        }
        return token.toString();
    }

    // Secure cryptographic hashing - BCrypt for password storage
    public String hashPassword(String password) {
        return passwordEncoder.encode(password);
    }

    // Verify password against BCrypt hash
    public boolean verifyPassword(String rawPassword, String hashedPassword) {
        return passwordEncoder.matches(rawPassword, hashedPassword);
    }

    // Secure session ID generation using SecureRandom
    public String generateSessionId() {
        long sessionId = secureRandom.nextLong();
        return Long.toHexString(sessionId);
    }

    // Secure XML parsing with XXE protection
    public String parseUserDataXml(String xmlContent) {
        try {
            javax.xml.parsers.DocumentBuilderFactory factory = javax.xml.parsers.DocumentBuilderFactory.newInstance();
            // Disable external entity processing to prevent XXE attacks
            factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
            factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
            factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
            factory.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);
            factory.setXIncludeAware(false);
            factory.setExpandEntityReferences(false);
            factory.setAttribute("http://javax.xml.XMLConstants/feature/secure-processing", Boolean.TRUE);
            
            javax.xml.parsers.DocumentBuilder builder = factory.newDocumentBuilder();
            java.io.ByteArrayInputStream input = new java.io.ByteArrayInputStream(xmlContent.getBytes());
            org.w3c.dom.Document doc = builder.parse(input);
            return doc.getDocumentElement().getTextContent();
        } catch (Exception e) {
            throw new XmlParsingException("Failed to parse XML content", e);
        }
    }

}
