import streamlit as st
import mysql.connector

### Run `streamlit run airbnb_gui.py` in the terminal to start the app

def get_connection(user='root', password=None):
    return mysql.connector.connect(
        user = 'root',
        password = password,
        host = 'localhost',
        database = 'Airbnb'
    )

def neighborhoods_with_highest_listing_density(city):
    sql = """
        SELECT LOC.Neighborhood, COUNT(*) AS ListingCount
        FROM Listing L
        JOIN Location LOC ON L.LocationId = LOC.LocationId
        WHERE LOC.City = %s
        GROUP BY LOC.Neighborhood
        ORDER BY ListingCount DESC;
    """
    return sql, (city,)

def listing_order_by_overall_rating(city):
    sql = """
        SELECT L.ListingId, L.ListingName, RT.OverallScore, LP.`Price/Night`
        FROM Listing L
        JOIN Rating RT ON L.ListingId = RT.ListingId
        JOIN Location LOC ON L.LocationId = LOC.LocationId
        JOIN ListingProfile LP ON L.ListingId = LP.ListingId
        WHERE LOC.City = %s
        ORDER BY RT.OverallScore DESC;
    """
    return sql, (city,)

def top_listings_in_city_with_excellent_ratings(city):
    sql = """
        SELECT L.ListingId, L.ListingName, AVG(RT.OverallScore) AS AvgRating, COUNT(RV.ReviewId) AS ReviewCount
        FROM Listing L 
        JOIN Location LOC ON L.LocationId = LOC.LocationId
        JOIN Rating RT ON L.ListingId = RT.ListingId
        JOIN Review RV ON L.ListingId = RV.ListingId
        WHERE LOC.City = %s
        GROUP BY L.ListingName, L.ListingId 
        HAVING AvgRating > 95 AND ReviewCount >= 20
        ORDER BY AvgRating DESC;
    """
    return sql, (city,)

def top_neighborhoods_by_review_score(city):
    sql = """
        SELECT LOC.Neighborhood, AVG(RT.OverallScore) AS AvgScore
        FROM Listing L
        JOIN Location LOC ON L.LocationId = LOC.LocationId
        JOIN Rating RT ON L.ListingId = RT.ListingId
        WHERE LOC.City = %s
        GROUP BY LOC.Neighborhood
        ORDER BY AvgScore DESC;
    """
    return sql, (city,)

def most_reviewed_neighborhoods_average_price(city):
    sql = """
        SELECT LOC.Neighborhood, COUNT(RV.ReviewId) AS TotalReviews, AVG(LP.`Price/Night`) AS AvgPrice
        FROM Listing L
        JOIN Location LOC ON L.LocationId = LOC.LocationId
        JOIN Review RV ON L.ListingId = RV.ListingId
        JOIN ListingProfile LP ON L.ListingId = LP.ListingId
        WHERE LOC.City = %s
        GROUP BY LOC.Neighborhood
        ORDER BY TotalReviews DESC;
    """
    return sql, (city,)

def neighborhoods_with_high_ratings_little_reviews(city):
    sql = """
        SELECT LOC.Neighborhood, L.ListingId, L.ListingName, AVG(RT.OverallScore) AS AvgRating, COUNT(RV.ReviewId) AS ReviewCount
        FROM Listing L
        JOIN Location LOC ON L.LocationId = LOC.LocationId
        JOIN Rating RT ON L.ListingId = RT.ListingId
        JOIN Review RV ON L.ListingId = RV.ListingId
        WHERE LOC.City = %s
        GROUP BY LOC.Neighborhood, L.ListingId, L.ListingName
        HAVING AvgRating > 95 AND ReviewCount < 5 
        ORDER BY LOC.Neighborhood, AvgRating DESC;
    """
    return sql, (city,)

def neighborhood_with_high_cleanliness_communication(city):
    sql = """
        SELECT LOC.Neighborhood, AVG(RT.Cleanliness) AS AvgCleanliness, AVG(RT.Communication) AS AvgCommunication
        FROM Listing L
        JOIN Location LOC ON L.LocationId = LOC.LocationId
        JOIN Rating RT ON L.ListingId = RT.ListingId
        WHERE LOC.City = %s
        GROUP BY LOC.Neighborhood
        ORDER BY AvgCleanliness DESC, AvgCommunication DESC;
    """
    return sql, (city,)

def listings_with_workspace_wifi(city):
    sql = """
    SELECT L.ListingId, L.ListingName, (LP.`Price/Night`) AS Price
    FROM Listing L
    JOIN ListingAmenities LA ON L.ListingId = LA.ListingId
    JOIN Amenity A ON LA.AmenityId = A.AmenityId
    JOIN ListingProfile LP ON L.ListingId = LP.ListingId
    JOIN Location LOC ON L.LocationId = LOC.LocationId
    WHERE A.AmenityName IN ('Wi-Fi', 'Dedicated workspace') AND LOC.City = %s
    ORDER BY Price ASC;
    """
    return sql, (city,)

def listings_with_hot_tub_2_more_bedrooms(city):
    sql = """
        SELECT L.ListingId, L.ListingName, (LP.`Price/Night`) AS Price, LP.`Bedroom#` AS Bedrooms
        FROM Listing L
        JOIN ListingAmenities LA ON L.ListingId = LA.ListingId
        JOIN Amenity A ON LA.AmenityId = A.AmenityId
        JOIN ListingProfile LP ON L.ListingId = LP.ListingId
        JOIN Location LOC ON L.LocationId = LOC.LocationId
        WHERE A.AmenityName = 'Hot tub' AND LP.`Bedroom#` > 2 AND LOC.City = %s
        ORDER BY Price ASC;
    """
    return sql, (city,)

def listings_accommodate_large_party(city):
    sql = """
        SELECT L.ListingId, L.ListingName
        FROM Listing L
        JOIN ListingAmenities LA ON L.ListingId = LA.ListingId
        JOIN Amenity A ON LA.AmenityId = A.AmenityId
        JOIN ListingProfile LP ON L.ListingId = LP.ListingId
        JOIN Location LOC ON L.LocationId = LOC.LocationId
        WHERE LP.`Accommodate#` > 6 AND LOC.City = %s
        GROUP BY ListingID;
    """
    return sql, (city,)

def high_rated_listings_few_reviews(city):
    sql = """
        SELECT L.ListingId, L.ListingName, COUNT(RV.ReviewId) AS ReviewCount, AVG(RT.OverallScore) AS AvgRating, 
            (LP.`Price/Night`) AS Price
        FROM Listing L
        JOIN Review RV ON L.ListingId = RV.ListingId
        JOIN Rating RT ON L.ListingId = RT.ListingId
        JOIN ListingProfile LP ON L.ListingId = LP.ListingId
        JOIN Location LOC ON L.LocationId = LOC.LocationId
        WHERE LOC.City = %s
        GROUP BY L.ListingId, L.ListingName, Price
        HAVING ReviewCount < 5 AND AvgRating > 95
        ORDER BY AvgRating DESC;
    """
    return sql, (city,)

def listings_consistent_5_star_ratings(city):
    sql = """
        SELECT L.ListingId, L.ListingName, (LP.`Price/Night`) AS Price
        FROM Listing L
        JOIN Rating RT ON L.ListingId = RT.ListingId
        JOIN ListingProfile LP ON L.ListingId = LP.ListingId
        JOIN Location LOC ON L.LocationId = LOC.LocationId
        WHERE LOC.City = %s
        GROUP BY L.ListingId, L.ListingName, Price
        HAVING MIN(RT.OverallScore) = 100
        Order by Price ASC;
    """
    return sql, (city,)

def listings_high_availability_great_ratings(accomomodate, price):
    sql = """
        SELECT L.ListingId, L.ListingName, COUNT(RV.ReviewId) AS ReviewCount, AVG(RT.OverallScore) AS AvgRating
        FROM Listing L
        JOIN ListingProfile LP ON L.ListingId = LP.ListingId
        JOIN Rating RT ON L.ListingId = RT.ListingId
        JOIN Review RV ON L.ListingId = RV.ListingId
        WHERE LP.`Accommodate#` > %s
          AND LP.`Price/Night` < %s 
        GROUP BY L.ListingId, L.ListingName
        HAVING COUNT(RV.ReviewId) >= 10 AND AvgRating > 90 
        ORDER BY AvgRating DESC;
    """
    return sql, (accomomodate, price)

def compare_cleanliness_communication_by_city(city):
    sql = """
        SELECT RT.RoomTypeName,
            AVG(RTNG.Cleanliness) AS AvgCleanliness,
            AVG(RTNG.Communication) AS AvgCommunication, 
            AVG(LP.`Price/Night`) AS AvgPrice
        FROM Listing L
        JOIN RoomType RT ON L.RoomTypeId = RT.RoomTypeId
        JOIN Rating RTNG ON L.ListingId = RTNG.ListingId
        JOIN ListingProfile LP ON L.ListingId = LP.ListingId
        JOIN Location LOC ON L.LocationId = LOC.LocationId
        WHERE LOC.City = %s
        GROUP BY RT.RoomTypeName;
    """
    return sql, (city,)

def compare_prices_by_neighborhood(city):
    sql = """
        SELECT LOC.Neighborhood, AVG(LP.`Price/Night`) AS AvgPrice, AVG(RT.OverallScore) AS AvgRating
        FROM Listing L
        JOIN Location LOC ON L.LocationId = LOC.LocationId
        JOIN ListingProfile LP ON L.ListingId = LP.ListingId
        JOIN Rating RT ON L.ListingId = RT.ListingId
        WHERE LOC.City = %s
        GROUP BY LOC.Neighborhood
        ORDER BY AvgPrice ASC;
    """
    return sql, (city,)

def visited_listings(name):
    sql = """
        SELECT L.ListingId, L.ListingName, LOC.City
        FROM Review RV
        JOIN Guest G ON RV.GuestId = G.GuestId
        JOIN Listing L ON RV.ListingId = L.ListingId
        JOIN Location LOC ON L.LocationId = LOC.LocationId
        WHERE G.GuestName = %s
        GROUP BY L.ListingId, L.ListingName, LOC.City;
    """
    return sql, (name,)

def reviewed_listings(name):
    sql = """
        SELECT LOC.City, COUNT(*) AS ReviewCount
        FROM Review RV
        JOIN Listing L ON RV.ListingId = L.ListingId
        JOIN Location LOC ON L.LocationId = LOC.LocationId
        JOIN Guest G ON RV.GuestId = G.GuestId
        WHERE G.GuestName = %s
        GROUP BY LOC.City
        ORDER BY ReviewCount DESC;
    """
    return sql, (name,)

def visited_poorly_rated_listings(name):
    sql = """
        SELECT L.ListingId, L.ListingName, RT.OverallScore, LOC.City
        FROM Review RV
        JOIN Listing L ON RV.ListingId = L.ListingId
        JOIN Rating RT ON L.ListingId = RT.ListingId
        JOIN Guest G ON RV.GuestId = G.GuestId
        JOIN Location LOC ON L.LocationId = LOC.LocationId
        WHERE G.GuestName = %s
          AND RT.OverallScore < 90
        ORDER BY RT.OverallScore ASC;
    """
    return sql, (name,)

def non_visited_listings_in_visited_cities(name):
    sql = """
        SELECT DISTINCT L.ListingId, L.ListingName, (LP.`Price/Night`) AS AvgPrice, RT.OverallScore
        FROM Review RV
        JOIN Listing L ON RV.ListingId = L.ListingId
        JOIN Location LOC ON L.LocationId = LOC.LocationId
        JOIN ListingProfile LP ON L.ListingId = LP.ListingId
        JOIN Guest G ON RV.GuestId = G.GuestId
        JOIN Rating RT ON L.ListingId = RT.ListingId
        WHERE LOC.City IN (
          SELECT DISTINCT LOC.City
          FROM Review RV
          JOIN Listing L2 ON RV.ListingId = L2.ListingId
          JOIN Location LOC ON L2.LocationId = LOC.LocationId
          JOIN Guest G ON RV.GuestId = G.GuestId
          WHERE G.GuestName = %s
        )
        AND L.ListingId NOT IN (
          SELECT ListingId 
          FROM Review 
          JOIN Guest G ON RV.GuestId = G.GuestId
          WHERE G.GuestName = %s
        )
        ORDER BY OverallScore DESC;
    """
    return sql, (name,)

def previously_booked_hosts(name):
    sql = """
        SELECT DISTINCT H.FirstName, H.LastName, H.HostId
        FROM Review RV
        JOIN Listing L ON RV.ListingId = L.ListingId
        JOIN Host H ON L.HostId = H.HostId
        JOIN Guest G ON RV.GuestId = G.GuestId
        WHERE G.GuestName = %s;
    """
    return sql, (name,)

def avg_review_scored_per_room_type_in_city(city):
    sql = """
        SELECT RT.RoomTypeName, AVG(RR.OverallScore) AS AvgRating
        FROM Listing AS L
        JOIN RoomType AS RT ON L.RoomTypeId = RT.RoomTypeId
        JOIN Location AS LC ON L.LocationId = LC.LocationId
        JOIN Rating AS RR ON L.ListingId = RR.ListingId
        GROUP BY RT.RoomTypeName;
        Having LC.City = %s;
    """
    return sql, (city,)

def hosts_with_given_listings_and_avg_ratings(avg_rating, listings):
    sql = """
        SELECT DISTINCT H.HostId, H.FirstName, H.LastName, AVG(RR.OverallScore) AS AvgRating
        FROM Host AS H
        JOIN Listing AS L ON H.HostId = L.HostId
        JOIN Rating AS RR ON L.ListingId = RR.ListingId
        WHERE RR.OverallScore > %s
        GROUP BY H.HostId
        HAVING COUNT(L.ListingId) > %s;
    """
    return sql, (avg_rating, listings)

def listings_by_host_id_starting_with(starting):
    sql = """
        SELECT ListingId, ListingName
        FROM Listing
        WHERE HostId LIKE '%s%%';
    """
    return sql, (starting,)

def top_n_listings_by_overall_rating_scores_in_city_district(city, distict, n):
    sql = """
        SELECT L.ListingId, R.OverallScore, R.Cleanliness, R.Accuracy, R.Value, R.Communication
        FROM Listing AS L
        JOIN Location AS LC ON L.LocationId = LC.LocationId
        JOIN Rating AS R ON L.ListingId = R.ListingId
        WHERE LC.City = %s AND LC.District = %s
        ORDER BY R.OverallScore DESC
        LIMIT %s;
    """
    return sql, (city, distict, n)

def guest_activity_for_given_host(host_id):
    sql = """
        SELECT L.ListingId, L.ListingName, G.GuestName, R.Date
        FROM Listing AS L
        JOIN Review AS R ON L.ListingId = R.ListingId
        JOIN Guest AS G ON R.GuestId = G.GuestId
        WHERE L.HostId = %s
        ORDER BY R.Date DESC;
    """
    return sql, (host_id,)

def least_rated_listings_in_city_more_than_price(city, price):
    sql = """
        SELECT L.ListingId, LC.Neighborhood, RR.OverallScore
        FROM Listing AS L
        JOIN Location AS LC ON L.LocationId = LC.LocationId
        JOIN Rating AS RR ON L.ListingId = RR.ListingId
        JOIN ListingProfile AS LP ON L.ListingId = LP.ListingId
        WHERE LC.City = %s AND LP.`Price/Night` > %s
        AND RR.OverallScore IS NOT NULL
        ORDER BY RR.OverallScore ASC;
    """
    return sql, (city, price)

def listings_with_year_review_and_avg_rating_below(year, rating):
    sql = """
        SELECT L.ListingId, AVG(RR.OverallScore) AS AvgRating
        FROM Listing AS L
        JOIN Rating AS RR ON L.ListingId = RR.ListingId
        JOIN Review AS R ON R.ListingId = L.ListingId
        WHERE YEAR(R.Date) = %s
        GROUP BY L.ListingId
        HAVING AvgRating < %s;
    """
    return sql, (year, rating)

def top_cities_by_num_active_listings(n):
    sql = """
        SELECT LC.City, COUNT(L.ListingId) AS TotalListings
        FROM Listing L
        JOIN Location LC ON L.LocationId = LC.LocationId
        GROUP BY LC.City
        ORDER BY TotalListings DESC;
        LIMIT %s;
    """
    return sql, (n,)

def all_reviews_by_guest(guest_id):
    sql = """
        SELECT rv.ReviewId, rv.Date, l.ListingName
        FROM Review rv
        JOIN Listing l ON rv.ListingId = l.ListingId
        WHERE rv.GuestId = 126;
    """
    return sql, (guest_id,)

def lowest_rated_listings_by_host(host_id):
    sql = """
    SELECT l.ListingId, l.HostId
    FROM Listing l
    WHERE l.HostId = %s
    AND l.ListingId IN (
        SELECT l.ListingId
        FROM Listing l
        LEFT JOIN Review r ON l.ListingId = r.ListingId
        GROUP BY l.ListingId
        HAVING COUNT(r.ReviewId) = (
            SELECT MIN(ReviewCount)
            FROM (
                SELECT COUNT(r2.ReviewId) AS ReviewCount
                FROM Listing l2
                LEFT JOIN Review r2 ON l2.ListingId = r2.ListingId
                WHERE l2.HostId = l.HostId
                GROUP BY l2.ListingId
            ) AS review_counts
        )
        UNION
        SELECT l.ListingId
        FROM Listing l
        JOIN Rating ra ON l.ListingId = ra.ListingId
        WHERE ra.OverallScore = (
            SELECT MIN(ra2.OverallScore)
            FROM Listing l2
            JOIN Rating ra2 ON l2.ListingId = ra2.ListingId
            WHERE l2.HostId = l.HostId)
    );
    """
    return sql, (host_id,)

INTERNAL_OPS = {
    "Listings that have received reviews for a given year but have an average overall rating below a certain threshold": {
        "inputs": ["year", "rating"],
        "query_func": listings_with_year_review_and_avg_rating_below,
    },
    "Identify listings that are most frequently reviewed by guests who tend to leave high ratings": 
        """
        SELECT L.ListingId, COUNT(R.ReviewId) AS ReviewCount
        FROM Listing AS L
        JOIN Review AS R ON L.ListingId = R.ListingId
        JOIN Guest AS G ON R.GuestId = G.GuestId
        WHERE G.AvgRatingLeft > 4.5
        GROUP BY L.ListingId
        ORDER BY ReviewCount DESC;
        """,
    "List guests who have reviewed listings in two or more different cities":
        """
        SELECT G.GuestName
        FROM Guest AS G
        JOIN Review AS R ON G.GuestId = R.GuestId
        JOIN Listing AS L ON R.ListingId = L.ListingId
        JOIN Location AS LC ON L.LocationId = LC.LocationId
        GROUP BY G.GuestId
        HAVING COUNT(DISTINCT LC.City) >= 2;
        """,
    "Top n cities by number of active listings":{
            "inputs": ["n"],
            "query_func": top_cities_by_num_active_listings,
    },
    "Playform-wide average ratings":
        """
        SELECT AVG(OverallScore) AS AvgRating, AVG(Cleanliness) AS AvgCleanliness,
              AVG(Accuracy) AS AvgAccuracy, AVG(Value) AS AvgValue, AVG(Communication) AS AvgCommunication
        FROM Rating;
        """,
    "All reviews by a given guest": {
        "inputs": ["guest_id"],
        "query_func": all_reviews_by_guest,
    },
    "Superhost rate":
        """
        SELECT 
            COUNT(CASE WHEN IsSuper = 1 THEN 1 END) * 100.0 / COUNT(*) AS SuperhostRate
            FROM Host;
        """
}

HOST_QUERY_MAP = {
    "Listings that receive  significantly fewer reviews or lower ratings than the host's other listings for a given host": {
        "inputs": ["host_id"],
        "query_func": lowest_rated_listings_by_host,
    },
    "Show the average review scores per room type in a given city": {
        "inputs": ["city"],
        "query_func": avg_review_scored_per_room_type_in_city,
    },
    "Rank all room types by their average number of reviews per listing":
        """
        SELECT RT.RoomTypeName, AVG(ReviewCount) AS AvgNumReviews
        FROM (
            SELECT L.ListingId, L.RoomTypeId, COUNT(R.ReviewId) AS ReviewCount
            FROM Listing AS L
            RIGHT JOIN Review AS R ON L.ListingId = R.ListingId
            GROUP BY L.ListingId
            ) AS LR
        JOIN RoomType AS RT ON LR.RoomTypeId = RT.RoomTypeId
        GROUP BY RT.RoomTypeName
        ORDER BY AvgNumReviews DESC;
        """,
    "Hosts with a given number of listings and average ratings above a certain threshold": {
            "inputs": ["avg_rating", "listings"],
            "query_func": hosts_with_given_listings_and_avg_ratings,
    },
    "Listings by host ID starting with a specific prefix": {
            "inputs": ["starting"],
            "query_func": listings_by_host_id_starting_with,
    },
    "See top n Listings by overall rating scores in city district": {
        "inputs": ["city", "district", "n"],
        "query_func": top_n_listings_by_overall_rating_scores_in_city_district,
    },
    "Guest activity for a given host": {
        "inputs": ["host_id"],
        "query_func": guest_activity_for_given_host,
    },
    "Least rated listings in a city with a price above a certain threshold": {
        "inputs": ["city", "price"],
        "query_func": least_rated_listings_in_city_more_than_price,
    }
}

QUERY_MAP = {
    "Exploratory Queries": {
        "Most popular cities by number of listing": 
            """
            SELECT LOC.City, COUNT(*) AS TotalListings
            FROM Listing L
            JOIN Location LOC ON L.LocationId = LOC.LocationId
            GROUP BY LOC.City
            ORDER BY TotalListings DESC;
            """,
        "Most Common Room Types Across All Listings":
            """
            SELECT RT.RoomTypeName, COUNT(*) AS Count
            FROM Listing L
            JOIN RoomType RT ON L.RoomTypeId = RT.RoomTypeId
            GROUP BY RT.RoomTypeName
            ORDER BY Count DESC;
            """,
        "Neighborhoods with the Highest Listing Density in a City": {
            "inputs": ["city"],
            "query_func": neighborhoods_with_highest_listing_density,
        },
        "Listing Order by Overall Rating for a given city": {
            "inputs": ["city"],
            "query_func": listing_order_by_overall_rating,
        }
    },
    "Location-Based Recommendations": {
        "Top Listings in a City with Excellent Ratings": {
            "inputs": ["city"],
            "query_func": top_listings_in_city_with_excellent_ratings,
        },
        "Top Neighborhoods by Review Score in a City": {
            "inputs": ["city"],
            "query_func": top_neighborhoods_by_review_score,
        },
        "Most Reviewed Neighborhoods (High Guest Activity) with Average Price": {
            "inputs": ["city"],
            "query_func": most_reviewed_neighborhoods_average_price,
        },
        "Neighborhoods with High Ratings but Few Reviews in a City": {
            "inputs": ["city"],
            "query_func": neighborhoods_with_high_ratings_little_reviews,
        },
        "Neighborhood with High Cleanliness and Communication Ratings in a City": {
            "inputs": ["city"],
            "query_func": neighborhood_with_high_cleanliness_communication,
        }
    },
    "Feature & Amenity Filters": {
        "Listings with Workspace and Wi-Fi in a City": {
            "inputs": ["city"],
            "query_func": listings_with_workspace_wifi,
        },
        "Listings with Hot Tub and 2+ Bedrooms in a City": {
            "inputs": ["city"],
            "query_func": listings_with_hot_tub_2_more_bedrooms,
        },
        "Listings that Accommodate Large Parties in a City": {
            "inputs": ["city"],
            "query_func": listings_accommodate_large_party,
        }   
    },
    "Rating & Price Trends": {
        "High-Rated Listings with Few Reviews in a City": {
            "inputs": ["city"],
            "query_func": high_rated_listings_few_reviews,
        },
        "Listings with Consistent 5-Star Ratings in a City": {
            "inputs": ["city"],
            "query_func": listings_consistent_5_star_ratings,
        },
        "Listings with High Availability and Great Ratings": {
            "inputs": ["accommodate", "price"],
            "query_func": listings_high_availability_great_ratings,
        }
    },
    "Informed Comparisons for Decision Making": {
        "Compare Cleanliness and Communication by City": {
            "inputs": ["city"],
            "query_func": compare_cleanliness_communication_by_city,
        },
        "Compare Prices by Neighborhood in a City": {
            "inputs": ["city"],
            "query_func": compare_prices_by_neighborhood,
        }    
    },
    "Personalized Discovery": {
        "Listings You've Visited": {
            "inputs": ["name"],
            "query_func": visited_listings,
        },
        "Cities You've Reviewed by Order": {
            "inputs": ["name"],
            "query_func": reviewed_listings,
        },
        "Listings You've Visited But Rated Poorly": {
            "inputs": ["name"],
            "query_func": visited_poorly_rated_listings,
        },
        "Listings You Haven’t Tried Yet in Cities You Visited": {
            "inputs": ["name"],
            "query_func": non_visited_listings_in_visited_cities,
        },
        "Hosts You've Booked From Before": {
            "inputs": ["name"],
            "query_func": previously_booked_hosts,
        }
    }
}

QUERY_TYPES = {
    "Host Queries": HOST_QUERY_MAP,
    "Guest Queries": QUERY_MAP,
    "Internal Ops": INTERNAL_OPS
}

def login_screen():
    st.title("MySQL Login")

    with st.form("login_form"):
        user = st.text_input("Username")
        password = st.text_input("Password", type="password")
        option = st.radio("What would you like to do?", ["Insert Rating", "Run a Query"])
        submitted = st.form_submit_button("Login")

        if submitted:
            conn = get_connection(user, password)
            if conn:
                st.session_state["conn"] = conn
                st.session_state["logged_in"] = True
                if option == "Insert Rating":
                    st.session_state["page"] = "insert_rating"
                else:
                    st.session_state["page"] = "query_page"

def insert_rating_page():
    st.title("Insert New Rating")

    if st.button("Go to Query Page"):
        st.session_state["page"] = "query_page"

    listing_id = st.number_input("Listing ID", min_value=0, max_value=99999999, step=1)
    rating_id = st.number_input("Rating ID", min_value=0, max_value=99999999, step=1)
    overall_score = st.number_input("Overall Score", min_value=1, max_value=100, step=1)
    cleanliness_score = st.number_input("Cleanliness Score", min_value=1, max_value=10, step=1)
    communication_score = st.number_input("Communication Score", min_value=1, max_value=10, step=1)
    accuracy_score = st.number_input("Accuracy Score", min_value=1, max_value=10, step=1)
    value_score = st.number_input("Value Score", min_value=1, max_value=10, step=1)

    if st.button("Submit Rating"):
        try:
            conn = st.session_state["conn"]
            cursor = conn.cursor()
            insert_sql = """
                INSERT INTO `Rating` (RatingId, ListingId, OverallScore, Cleanliness, Accuracy, Value, Communication)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            data = (rating_id, listing_id, overall_score, cleanliness_score, accuracy_score, value_score, communication_score)
            cursor.execute(insert_sql, data)
            conn.commit()
            cursor.close()
            st.success("Rating inserted successfully!")
        except mysql.connector.Error as e:
            st.error(f"Failed to insert: {e}")

def main_app():
    st.title("Airbnb Database Explorer")
    st.markdown("Welcome to the Airbnb Database Interface! Use the tools below to explore listings, ratings, trends, and more.")

    if st.button("Go to Insert Rating Page"):
        st.session_state["page"] = "insert_rating"

    select_query_type = st.selectbox("Select Query Type", list(QUERY_TYPES.keys()))
    if select_query_type == "Guest Queries":
        query_type = st.selectbox("Select Guest Query Type", list(QUERY_MAP.keys()))
        if query_type == "Exploratory Queries":
            query_type = "Exploratory Queries"
            query_list = list(QUERY_MAP['Exploratory Queries'].keys())
        elif query_type == "Location-Based Recommendations":
            query_type = "Location-Based Recommendations"
            query_list = list(QUERY_MAP['Location-Based Recommendations'].keys())
        elif query_type == "Feature & Amenity Filters":
            query_type = "Feature & Amenity Filters"
            query_list = list(QUERY_MAP['Feature & Amenity Filters'].keys())
        elif query_type == "Rating & Price Trends":
            query_type = "Rating & Price Trends"
            query_list = list(QUERY_MAP['Rating & Price Trends'].keys())
        elif query_type == "Informed Comparison for Decision Making":
            query_type = "Informed Comparison for Decision Making"
            query_list = list(QUERY_MAP['Informed Comparison for Decision Making'].keys())
        elif query_type == "Personalized Discovery":
            query_type = "Personalized Discovery"
            query_list = list(QUERY_MAP['Personalized Discovery'].keys())
        else:
            query_list = []
            st.error("Invalid query type selected.")
    else:
        query_list = list(QUERY_TYPES[select_query_type].keys())

    selected_query = st.radio("Select a query", query_list)

    if select_query_type == "Guest Queries":
        query_info = QUERY_MAP[query_type][selected_query]
    else:
        query_info = QUERY_TYPES[select_query_type][selected_query]

    if isinstance(query_info, dict):
        query_func = query_info['query_func']
        inputs = query_info['inputs']
        input_values = []
        for input_name in inputs:
            input_value = st.text_input(f"Enter {input_name}:")
            if input_name.lower() in ["n", "accommodate", "price", "avg_rating", "listings", "year"]:
                try:
                    input_value = int(input_value)
                except ValueError:
                    st.error(f"Invalid input for {input_name}. Please enter a number.")
                    st.stop()
            elif input_name.lower() in ["rating"]:
                try:
                    input_value = float(input_value)
                except ValueError:
                    st.error(f"Invalid input for {input_name}. Please enter a number.")
                    st.stop()
            input_values.append(input_value)
        sql, params = query_func(*input_values)
    else:
        sql = query_info
        params = ()

    # Query execution
    if st.button("Run Query"):
        try:
            conn = st.session_state.get("conn")
            cursor = conn.cursor(dictionary=True)

            cursor.execute(sql, params)

            results = cursor.fetchall()
            if results:
                st.dataframe(results)
            else:
                st.write("No results found.")

        except Exception as e:
            st.error(f"Error: {e}")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "page" not in st.session_state:
    st.session_state["page"] = "login"

if not st.session_state["logged_in"]:
    login_screen()
elif st.session_state["page"] == "insert_rating":
    insert_rating_page()
else: # elif st.session_state["page"] == "query_page":
    main_app()
