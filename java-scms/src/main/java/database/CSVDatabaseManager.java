package database;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class CSVDatabaseManager implements DatabaseManager {

    public static void main(String[] args) {
        DatabaseManager databaseManager = new CSVDatabaseManager();
        databaseManager.initialize();
    }


    @Override
    public void initialize() {
        Map<String, String[]> tables = new HashMap<>();
        tables.put("students", new String[] {"student_id", "name", "email", "password"});
        tables.put("courses", new String[]  {"instructor_id", "name", "email", "password"});
        tables.put("enrollments", new String[]  {"course_id", "title", "instructor_id"});
        tables.put("instructors", new String[]  {"student_id", "course_id", "grade"});

        for (Map.Entry<String, String[]> entry : tables.entrySet()) {
            String tableName = entry.getKey();
            String[] headers = entry.getValue();
            String path = tableName + ".csv";

            File table = new File(path);
            if (table.exists() == false) createTable(table, headers);
        }
    }

    private void createTable(File table, String[] headers) {
        try (FileWriter csvWriter = new FileWriter(table)) {
            csvWriter.write(String.join(",", headers) + "\n");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public String getFilePath(String tableName){
        return  tableName;
    }

    @Override
    public int getNextId(String tableName){
        return 0;
    }

    @Override
    public void save(String tableName, Map obj){
        System.out.println("Saved");
    }

    @Override
    public void update(String tableName, Map obj, String key, String value){

    }

    @Override
    public void delete(String tableName, String key, String value){

    }

    @Override
    public List<String[]> fetchAll(String tableName){
        return null;
    }

    @Override
    public List<String[]> filterRecords(String tableName, String key, String value){
        return List.of(new String[] {"Hello", "world"}, new String[] {"Hy", "mal"});
    }

    @Override
    public boolean recordExists(String value) {
        return false;
    }

    @Override
    public boolean recordExists(String value, String tableName){
        return false;
    }

}
