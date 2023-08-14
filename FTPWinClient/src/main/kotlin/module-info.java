module com.fwc.ftpwinclient {
    requires javafx.controls;
    requires javafx.fxml;
    requires kotlin.stdlib;


    opens com.fwc.ftpwinclient to javafx.fxml;
    exports com.fwc.ftpwinclient;
}