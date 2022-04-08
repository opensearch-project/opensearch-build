def call(Map args = [:]) {
    String testType = args.testType
    String status = args.status
    String absoluteUrl = args.absoluteUrl
    String icon = status == 'SUCCESS' ? ':white_check_mark:' : ':warning:'

    return "\n${testType}: ${icon} ${status} ${absoluteUrl}"
}