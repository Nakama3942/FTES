module com.fwc.ftpwinclient {
    requires javafx.controls;
    requires javafx.fxml;
    requires kotlin.stdlib;
    requires org.apache.commons.net;


    opens com.fwc.ftpwinclient to javafx.fxml;
    exports com.fwc.ftpwinclient;
}