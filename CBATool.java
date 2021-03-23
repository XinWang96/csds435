import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;


public class CBATool {
    public final String AGE = "Age";
    public final String AGE_YOUNG = "Young";
    public final String AGE_MIDDLE_AGED = "Middle_aged";
    public final String AGE_Senior = "Senior";

    private String filePath;
    private double minSupportRate;
    private double minConf;
    private int minSupportCount;
    private String[] attrNames;
    private ArrayList<Integer> classTypes;
    private ArrayList<String[]> totalDatas;
    private AprioriTool aprioriTool;
    private HashMap<String, Integer> attr2Num;
    private HashMap<Integer, String> num2Attr;

    public CBATool(String filePath, double minSupportRate, double minConf) {
        this.filePath = filePath;
        this.minConf = minConf;
        this.minSupportRate = minSupportRate;
        readDataFile();
    }


    private void readDataFile() {
        File file = new File(filePath);
        ArrayList<String[]> dataArray = new ArrayList<String[]>();

        try {
            BufferedReader in = new BufferedReader(new FileReader(file));
            String str;
            String[] tempArray;
            while ((str = in.readLine()) != null) {
                tempArray = str.split(" ");
                dataArray.add(tempArray);
            }
            in.close();
        } catch (IOException e) {
            e.getStackTrace();
        }

        totalDatas = new ArrayList<>();
        for (String[] array : dataArray) {
            totalDatas.add(array);
        }
        attrNames = totalDatas.get(0);
        minSupportCount = (int) (minSupportRate * totalDatas.size());

        attributeReplace();
    }


    private void attributeReplace() {
        int currentValue = 1;
        int num = 0;
        String s;
        attr2Num = new HashMap<>();
        num2Attr = new HashMap<>();
        classTypes = new ArrayList<>();

        for (int j = 1; j < attrNames.length; j++) {
            for (int i = 1; i < totalDatas.size(); i++) {
                s = totalDatas.get(i)[j];
                if (attrNames[j].equals(AGE)) {
                    num = Integer.parseInt(s);
                    if (num <= 20 && num > 0) {
                        totalDatas.get(i)[j] = AGE_YOUNG;
                    } else if (num > 20 && num <= 40) {
                        totalDatas.get(i)[j] = AGE_MIDDLE_AGED;
                    } else if (num > 40) {
                        totalDatas.get(i)[j] = AGE_Senior;
                    }
                }

                if (!attr2Num.containsKey(totalDatas.get(i)[j])) {
                    attr2Num.put(totalDatas.get(i)[j], currentValue);
                    num2Attr.put(currentValue, totalDatas.get(i)[j]);
                    if (j == attrNames.length - 1) {
                        classTypes.add(currentValue);
                    }

                    currentValue++;
                }
            }
        }

        for (int i = 1; i < totalDatas.size(); i++) {
            for (int j = 1; j < attrNames.length; j++) {
                s = totalDatas.get(i)[j];
                if (attr2Num.containsKey(s)) {
                    totalDatas.get(i)[j] = attr2Num.get(s) + "";
                }
            }
        }
    }


    private ArrayList<FrequentItem> aprioriCalculate() {
        String[] tempArray;
        ArrayList<FrequentItem> totalFrequentItems;
        ArrayList<String[]> copyData = (ArrayList<String[]>) totalDatas.clone();

        copyData.remove(0);
        for (int i = 0; i < copyData.size(); i++) {
            String[] array = copyData.get(i);
            tempArray = new String[array.length - 1];
            System.arraycopy(array, 1, tempArray, 0, tempArray.length);
            copyData.set(i, tempArray);
        }
        aprioriTool = new AprioriTool(copyData, minSupportCount);
        aprioriTool.computeLink();
        totalFrequentItems = aprioriTool.getTotalFrequentItems();

        return totalFrequentItems;
    }


    public String CBAJudge(String attrValues) {
        int value = 0;
        String classType = null;
        String[] tempArray;
        ArrayList<String> attrValueList = new ArrayList<>();
        ArrayList<FrequentItem> totalFrequentItems;

        totalFrequentItems = aprioriCalculate();
        String[] array = attrValues.split(",");
        for (String record : array) {
            tempArray = record.split("=");
            value = attr2Num.get(tempArray[1]);
            attrValueList.add(value + "");
        }

        for (FrequentItem item : totalFrequentItems) {
            if (item.getIdArray().length < (attrValueList.size() + 1)) {
                continue;
            }

            if (itemIsSatisfied(item, attrValueList)) {
                tempArray = item.getIdArray();
                classType = classificationBaseRules(tempArray);

                if (classType != null) {
                    classType = num2Attr.get(Integer.parseInt(classType));
                    break;
                }
            }
        }

        return classType;
    }


    private String classificationBaseRules(String[] items) {
        String classType = null;
        String[] arrayTemp;
        int count1 = 0;
        int count2 = 0;
        double confidenceRate;

        String[] noClassTypeItems = new String[items.length - 1];
        for (int i = 0, k = 0; i < items.length; i++) {
            if (!classTypes.contains(Integer.parseInt(items[i]))) {
                noClassTypeItems[k] = items[i];
                k++;
            } else {
                classType = items[i];
            }
        }

        for (String[] array : totalDatas) {
            arrayTemp = new String[array.length - 1];
            System.arraycopy(array, 1, arrayTemp, 0, array.length - 1);
            if (isStrArrayContain(arrayTemp, noClassTypeItems)) {
                count1++;

                if (isStrArrayContain(arrayTemp, items)) {
                    count2++;
                }
            }
        }


        confidenceRate = count1 * 1.0 / count2;
        if (confidenceRate >= minConf) {
            return classType;
        } else {
            return null;
        }
    }


    private boolean strIsContained(String[] array, String s) {
        boolean isContained = false;

        for (String str : array) {
            if (str.equals(s)) {
                isContained = true;
                break;
            }
        }

        return isContained;
    }


    private boolean isStrArrayContain(String[] array1, String[] array2) {
        boolean isContain = true;
        for (String s2 : array2) {
            isContain = false;
            for (String s1 : array1) {
                if (s2.equals(s1)) {
                    isContain = true;
                    break;
                }
            }

            if (!isContain) {
                break;
            }
        }

        return isContain;
    }


    private boolean itemIsSatisfied(FrequentItem item,
                                    ArrayList<String> attrValues) {
        boolean isContained = false;
        String[] array = item.getIdArray();

        for (String s : attrValues) {
            isContained = true;

            if (!strIsContained(array, s)) {
                isContained = false;
                break;
            }

            if (!isContained) {
                break;
            }
        }

        if (isContained) {
            isContained = false;

            for (Integer type : classTypes) {
                if (strIsContained(array, type + "")) {
                    isContained = true;
                    break;
                }
            }
        }

        return isContained;
    }

}
