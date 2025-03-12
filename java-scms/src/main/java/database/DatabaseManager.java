package database;

import java.util.List;
import java.util.Map;

public interface DatabaseManager {
    void initialize();
    String getFilePath(String tableName);
    int getNextId(String tableName);
    void save(String tableName, Map obj);
    void update(String tableName, Map obj, String key, String value);

    void delete(String tableName, String key, String value);
    List<String[]> fetchAll(String tableName);
    List<String[]> filterRecords(String tableName, String key, String value);

    boolean recordExists(String value);

    boolean recordExists(String value, String tableName);

}
