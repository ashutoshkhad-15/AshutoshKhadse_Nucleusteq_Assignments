package com.ashutosh.session2.service;

import com.ashutosh.session2.component.formatter.MessageFormatter;
import org.springframework.stereotype.Service;
import java.util.Map;

@Service
public class MessageService {

    private final Map<String, MessageFormatter> formatterMap;

    public MessageService(Map<String, MessageFormatter> formatterMap) {
        this.formatterMap = formatterMap;
    }

    public String getFormattedMessage(String type, String payload) {
        String normalizedType = type.toUpperCase();
        MessageFormatter formatter = formatterMap.get(normalizedType);

        if (formatter == null) {
            throw new IllegalArgumentException(
                    "Unsupported message type: '" + type + "'. Supported types: SHORT, LONG"
            );
        }

        return formatter.format(payload);
    }
}
