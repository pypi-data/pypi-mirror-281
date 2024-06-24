
const consts = {
        PROJECT_NONE: 1,
        PROJECT_NO_PROJECT: 2,
        PROJECT_LOADING: 3,
        PROJECT_ERROR: 4,
        PROJECT_NOT_LOGGED: 5,
        PROJECT_LOGGED: 6,
        PROJECT_MAINTAINANCE: 7,
        PROJECT_MODIFIED: 8,
        RESPONSE: 9,

        TEXT: 1,
        INTEGER: 2,
        FLOAT: 3,
        CURRENCY: 4,
        DATE: 5,
        DATETIME: 6,
        BOOLEAN: 7,
        LONGTEXT: 8,
        KEYS: 9,
        FILE: 10,
        IMAGE: 11,

        ITEM_FIELD: 1,
        FILTER_FIELD: 2,
        PARAM_FIELD: 3,

        FILTER_EQ: 1,
        FILTER_NE: 2,
        FILTER_LT: 3,
        FILTER_LE: 4,
        FILTER_GT: 5,
        FILTER_GE: 6,
        FILTER_IN: 7,
        FILTER_NOT_IN: 8,
        FILTER_RANGE: 9,
        FILTER_ISNULL: 10,
        FILTER_EXACT: 11,
        FILTER_CONTAINS: 12,
        FILTER_STARTWITH: 13,
        FILTER_ENDWITH: 14,
        FILTER_CONTAINS_ALL: 15,
        FILTER_EQ_L: 16,
        FILTER_NE_L: 17,
        FILTER_LT_L: 18,
        FILTER_LE_L: 19,
        FILTER_GT_L: 20,
        FILTER_GE_L: 21,
        FILTER_IN_L: 22,
        FILTER_NOT_IN_L: 23,
        FILTER_RANGE_L: 24,
        FILTER_ISNULL_L: 25,
        FILTER_EXACT_L: 26,
        FILTER_CONTAINS_L: 27,
        FILTER_STARTWITH_L: 28,
        FILTER_ENDWITH_L: 29,
        FILTER_CONTAINS_ALL_L: 30,

        ALIGN_LEFT: 1,
        ALIGN_CENTER: 2,
        ALIGN_RIGHT: 3,

        STATE_INACTIVE: 0,
        STATE_BROWSE: 1,
        STATE_INSERT: 2,
        STATE_EDIT: 3,
        STATE_DELETE: 4,

        RECORD_UNCHANGED: null,
        RECORD_INSERTED: 1,
        RECORD_MODIFIED: 2,
        RECORD_DELETED: 3,
        RECORD_DETAILS_MODIFIED: 4,

        REC_STATUS: 0,
        REC_LOG_REC: 1,

        UPDATE_OPEN: 0,
        UPDATE_RECORD: 1,
        UPDATE_APPEND: 2,
        UPDATE_INSERT: 3,
        UPDATE_SCROLLED: 4,
        UPDATE_CONTROLS: 5,
        UPDATE_CLOSE: 6,
        UPDATE_STATE: 7,
        UPDATE_APPLIED: 8,
        UPDATE_SUMMARY: 9,
        UPDATE_REFRESH: 10,
        align_value: ['', 'left', 'center', 'right'],
        filter_value: [
            'eq', 'ne', 'lt', 'le', 'gt', 'ge', 'in', 'not_in',
            'range', 'isnull', 'exact', 'contains', 'startwith', 'endwith',
            'contains_all',
            'eq_l', 'ne_l', 'lt_l', 'le_l', 'gt_l', 'ge_l', 'in_l', 'not_in_l',
            'range_l', 'isnull_l', 'exact_l', 'contains_l', 'startwith_l', 'endwith_l',
            'contains_all_l'
       ],
        field_attr: [
            "ID",
            "field_name",
            "field_caption",
            "data_type",
            "field_size",
            "required",
            "lookup_item",
            "lookup_field",
            "lookup_field1",
            "lookup_field2",
            "edit_visible",
            "_read_only",
            "default",
            "default_value",
            "master_field",
            "_alignment",
            "lookup_values",
            "multi_select",
            "multi_select_all",
            "enable_typeahead",
            "field_help",
            "field_placeholder",
            "field_interface",
            "field_image",
            "field_file",
            "reserved",
            "calculated"
        ],
        filter_attr: [
            "filter_name",
            "filter_caption",
            "field_name",
            "filter_type",
            "multi_select_all",
            "data_type",
            "visible",
            "filter_help",
            "filter_placeholder",
            "ID"
        ],
        field_type_names: ["", "text", "integer", "float", 'currency',
            "date", "datetime", "boolean", "longtext", "keys", "file", "image"
        ]
    }

export default consts
