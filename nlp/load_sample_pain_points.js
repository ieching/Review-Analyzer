// to be run in mongo shell
//
let timestamp = new Date()
let diddyriese_painpoints = [
    {
        title: "too sweet",
        description:"cookies are too sweet",
        solution: "Unsweeten cookies",
        example_review_ids: [
            "eaa03108-8789-455a-b89a-9741cbdd7361",
            "c58deff3-488b-4041-9343-53f3d587b9dd",
            "c51b4bba-cc95-4fd2-96a8-94d9ea004763",
            "4703ab80-79e5-4d53-8bf4-f76711548220"
        ]
    }, 
    {
        title: "Cash Only",
        description:"Customers must pay in Cash",
        solution: "Provide alternative payment solutions",
        example_review_ids: [
            "4c4fdb0d-c9ed-4569-b5f9-3e3b464bb2c8",
            "615f8501-4c94-481a-8729-f9fc5588e312",
            "e89317ba-8faa-463b-b13f-0c24de7ddf9e"
        ]
    },
    {
        title: "Parking",
        description:"Parking options are restricting",
        solution: "Provide better parking solutions",
        example_review_ids: [
            "e710b65e-7afd-44b5-95fa-52d616fa262d",
            "1f406758-b051-48dc-a73a-7ba6cb248475",
            "15f904de-202c-42f7-8734-8907f19b90f7"
        ]
    }
];

diddyriese_painpoints.forEach((d) => {
    d.source_id = "Yelp";
    d.business_id = "DiddyRiese"; 
    d.timestamp = timestamp;
})

db.painpoints.insertMany(diddyriese_painpoints);

let chickfila_painpoints = [
    {
        title: "Parking",
        description:"Limited parking spots",
        solution: "Provide better parking spots",
        example_review_ids: [
            "dcb91bac-624b-4f1a-928a-03b6faa91e9f",
            "61cb5d2d-5ea7-45ba-8648-b920b866d1c0"
        ]
    }, 
    {
        title: "Unfresh Food",
        description:"Food is not fresh",
        solution: "Examine food preparation techniques and equipment.",
        example_review_ids: [
            "c1a07b2d-a0c8-42c4-b86a-d40a05310cee",
            "a87a8c6a-3d23-4b70-bdd6-c8bb04bce7c4"
        ]
    },
];

chickfila_painpoints.forEach((d) => {
    d.source_id = "Yelp";
    d.business_id = "Chick-Fil-A"; 
    d.timestamp = timestamp;
})

db.painpoints.insertMany(chickfila_painpoints);

let simpang_painpoints = [
    {
        title: "Parking",
        description:"Limited parking spots",
        solution: "Provide better parking spots",
        example_review_ids: [
            "ccb24522-bd87-43d4-b4a2-45fd708e9fa3",
            "d685139f-af51-46a9-a2b4-e94aa386f8ae",
            "e0b2e49e-afa5-43bb-a0d5-e15b9de8ecd2"
        ]
    }, 
    {
        title: "Food is too salty",
        description:"Some dishes are too salty",
        solution: "Review food tasting.",
        example_review_ids: [
            "d1513709-8ddd-4f6e-83ab-6c59a85d6dde",
            "47dff47c-1819-454b-9c27-4254e564b6bd",
            "76eff9c3-72e6-4e14-8fe9-ba16853c2108"
        ]
    },
    {
        title: "Long wait",
        description:"Customers wait long for food",
        solution: "Review on-floor busyness and manpower.",
        example_review_ids: [
            "ef0b67d1-397f-451e-a5bc-928f43a5f5f3",
            "8fc0c5f8-c0cc-4dfb-811a-4f76fd719224",
            "4e1e67d7-ad61-43d4-8c26-e223f8ab6264"
        ]
    }
];

simpang_painpoints.forEach((d) => {
    d.source_id = "Yelp";
    d.business_id = "SimpangAsia"; 
    d.timestamp = timestamp;
})

db.painpoints.insertMany(simpang_painpoints);
