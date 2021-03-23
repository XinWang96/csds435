import java.text.MessageFormat;


public class Client {
    public static void main(String[] args){
        String filePath = "";
        String attrDesc = "Age=Senior,CreditRating=Fair";
        String classification = null;

        double minSupportRate = 0.2;
        double minConf = 0.7;

        CBATool tool = new CBATool(filePath, minSupportRate, minConf);
        classification = tool.CBAJudge(attrDesc);
        System.out.println(MessageFormat.format("", attrDesc, classification));
    }
}
