import asyncio
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


USER_EMAIL = "sandeepkurmadasu7@gmail.com"
USER_PASSWORD = "Sandeep@4"
GRAPHQL_URL = "http://127.0.0.1:8000/graphql/"

server = Server("learning_platform_tools")

current_user = {
    "user_id": None,
    "name": None,
    "email": None,
    "token": None,
    "is_logged_in": False
}



async def execute_graphql(query: str, variables: dict = None):

    async with httpx.AsyncClient() as client:
        response = await client.post(
            GRAPHQL_URL,
            json={"query": query, "variables": variables or {}},
            headers={"Content-Type": "application/json"},
            timeout=30.0
        )
        response.raise_for_status()
        return response.json()


async def auto_login():

    if current_user["is_logged_in"]:
        return True

    query = """
    mutation UserLogin($params: UserLogInReqParams!) {
        userLogin(params: $params) {
            ... on UserLoginResponseType {
                token
                user {
                    userId
                    email
                    name
                }
            }
            ... on NotExistedEmailFoundType {
                email
            }
            ... on WrongPasswordFoundType {
                password
            }
        }
    }
    """

    variables = {
        "params": {
            "email": USER_EMAIL,
            "password": USER_PASSWORD
        }
    }

    try:
        result = await execute_graphql(query, variables)
    except Exception as e:
        print(f"Auto-login error: {e}", flush=True)
        return False

    login_result = result["data"]["userLogin"]

    if "user" in login_result:
        user = login_result["user"]
        current_user["user_id"] = user["userId"]
        current_user["name"] = user["name"]
        current_user["email"] = user["email"]
        current_user["token"] = login_result.get("token")
        current_user["is_logged_in"] = True
        return True

    return False


async def handle_get_my_courses():

    query = """
    query GetUserEnrollments($params: GetUserEnrolledCourses!) {
        getUserEnrollments(params: $params) {
            ... on EnrollmentListType {
                enrollments {
                    courseId
                    courseTitle
                    courseStatus
                    coursePercentage
                    userLearningPathId
                }
            }
            ... on UserNotFoundType {
                userId
            }
        }
    }
    """

    variables = {"params": {"userId": current_user["user_id"]}}

    try:
        result = await execute_graphql(query, variables)
    except Exception as e:
        return f"Error: {str(e)}"

    enrollments = result["data"]["getUserEnrollments"].get("enrollments", [])

    if not enrollments:
        return f"Hi {current_user['name']}! You have no enrolled courses yet."

    response = f"Hi {current_user['name']}! Here are your enrolled courses:\n\n"
    total_progress = 0

    for i, course in enumerate(enrollments, 1):
        percentage = course['coursePercentage']
        total_progress += percentage

        filled = int(percentage / 5)
        bar = '█' * filled + '░' * (20 - filled)

        response += f"{i}. {course['courseTitle']}\n"
        response += f"   {bar} {percentage}%\n"
        response += f"   Status: {course['courseStatus']}\n"
        response += f"   Course : {course['courseTitle']}\n\n"

    avg_progress = total_progress // len(enrollments)
    response += f"Overall Average Progress: {avg_progress}%"

    return response


async def handle_get_course_progress(course_id: str):

    query = """
    query GetCourseCompletion($params: GetUserCourseCompletionReqParams!) {
        getUserCourseCompletionPercentage(params: $params) {
            ... on GetUserCourseCompletionPercentageType {
                courseId
                userId
                percentage
            }
            ... on CourseNotFoundType {
                courseId
            }
            ... on UserNotFoundType {
                userId
            }
        }
    }
    """

    variables = {
        "params": {
            "userId": current_user["user_id"],
            "courseId": course_id
        }
    }

    try:
        result = await execute_graphql(query, variables)
    except Exception as e:
        return f"Error: {str(e)}"

    percentage = result["data"]["getUserCourseCompletionPercentage"][
        "percentage"]

    filled = int(percentage / 5)
    bar = '█' * filled + '░' * (20 - filled)

    if percentage == 100:
        message = " Congratulations! You've completed this course!"
    elif percentage >= 75:
        message = "Great progress! You're almost there!"
    elif percentage >= 50:
        message = "You're halfway through! Keep going!"
    elif percentage >= 25:
        message = "Good start! Keep up the momentum!"
    else:
        message = "Just getting started! You got this!"

    response = f"Course Progress for {current_user['name']}\n\n"
    response += f"Course ID: {course_id}\n"
    response += f"Progress: {bar} {percentage}%\n\n"
    response += message

    return response


async def handle_get_learning_path_details(user_learning_path_id: str):

    query = """
    query GetLearningPathProgress($params: GetUserLearningUnitsReqParams!) {
        getUserLearningUnits(params: $params) {
            ... on UserLearningUnitsProgressType {
                units {
                    userLearningUnitId
                    topicId
                    moduleId
                    isLocked
                    percentage
                    status
                }
            }
            ... on UserLearningPathIdNotFoundType {
                userLearningPathId
            }
        }
    }
    """

    variables = {"params": {"userLearningPathId": user_learning_path_id}}

    try:
        result = await execute_graphql(query, variables)
    except Exception as e:
        return f"Error: {str(e)}"

    units = result["data"]["getUserLearningUnits"]["units"]

    if not units:
        return f"Learning Path Progress for {current_user['name']}\n\nNo units found in this learning path."

    completed = sum(1 for u in units if u["status"] == "COMPLETE")
    in_progress = sum(
        1 for u in units if u["status"] in ["IN_PROGRESS", "HALF_COMPLETED"])
    locked = sum(1 for u in units if u["isLocked"])
    overall_percentage = (completed / len(units) * 100) if units else 0

    response = f"Learning Path Progress for {current_user['name']}\n\n"
    response += f"Overall Completion: {int(overall_percentage)}%\n"
    response += f"Total Units: {len(units)}\n"
    response += f"Completed: {completed}\n"
    response += f"In Progress: {in_progress}\n"
    response += f"Locked: {locked}\n\n"
    response += "Unit Details:\n"
    response += "-" * 40 + "\n"

    for unit in units:
        status = unit["status"]

        if status == "COMPLETE":
            status_icon = "✅"
        elif status in ["IN_PROGRESS", "HALF_COMPLETE"]:
            status_icon = "🔄"
        else:
            status_icon = "🔒"

        percentage = unit['percentage']
        filled = int(percentage / 10)
        mini_bar = '█' * filled + '░' * (10 - filled)

        response += f"{status_icon} Unit {unit['userLearningUnitId']}: {mini_bar} {percentage}%\n"

    return response


async def handle_get_my_profile():

    query = """
    query GetUser($params: GetUserReqParms!) {
        getUser(params: $params) {
            ... on UserType {
                userId
                name
                username
                email
                phoneNumber
                gender
                isActive
            }
            ... on UserNotFoundType {
                userId
            }
        }
    }
    """

    variables = {"params": {"userId": current_user["user_id"]}}


    try:
        result = await execute_graphql(query, variables)
    except Exception as e:
        return f"Error: {str(e)}"

    user_result = result["data"]["getUser"]

    response = f"User Profile Information\n\n"
    response += f"Name: {user_result['name']}\n"
    response += f"Username: {user_result.get('username', 'N/A')}\n"
    response += f"Email: {user_result['email']}\n"
    response += f"Phone: {user_result.get('phoneNumber', 'N/A')}\n"
    response += f"Gender: {user_result.get('gender', 'N/A')}\n"
    response += f"Account Status: {'Active' if user_result.get('isActive', False) else 'Inactive'}\n"

    return response


@server.list_tools()
async def list_tools():

    return [
        Tool(
            name="get_my_courses",
            description="Get all my enrolled courses with completion percentages. No parameters needed - automatically uses logged-in user.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_course_progress",
            description="Get detailed completion percentage for a specific course by course ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "course_id": {
                        "type": "string",
                        "description": "The course ID to check progress for"
                    }
                },
                "required": ["course_id"]
            }
        ),
        Tool(
            name="get_learning_path_details",
            description="Get detailed learning path progress with all units by learning path ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_learning_path_id": {
                        "type": "string",
                        "description": "The learning path ID"
                    }
                },
                "required": ["user_learning_path_id"]
            }
        ),
        Tool(
            name="get_my_profile",
            description="Get my user profile information. No parameters needed.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):


    if not current_user["is_logged_in"]:
        login_success = await auto_login()
        if not login_success:
            return [TextContent(
                type="text",
                text="Failed to login. Please check credentials in server.py configuration."
            )]

    if name == "get_my_courses":
        result = await handle_get_my_courses()

    elif name == "get_course_progress":
        course_id = arguments.get("course_id")
        result = await handle_get_course_progress(course_id)

    elif name == "get_learning_path_details":
        user_learning_path_id = arguments.get("user_learning_path_id")
        result = await handle_get_learning_path_details(user_learning_path_id)

    elif name == "get_my_profile":
        result = await handle_get_my_profile()

    else:
        result = f"Unknown tool: {name}"

    return [TextContent(type="text", text=result)]


async def main():

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())