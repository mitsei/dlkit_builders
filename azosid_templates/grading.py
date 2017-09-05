class GradeEntryLookupSession:
    get_grade_entries_for_gradebook_column_on_date = """
        # Need to override this because there isn't a ``match_source_id`` method for OsidRelationshipQuery??
        if self._can('lookup'):
            return self._provider_session.get_grade_entries_for_gradebook_column_on_date(gradebook_column_id, from_, to)
        self._check_lookup_conditions()  # raises PermissionDenied
        raise PermissionDenied()
        # query = self._query_session.get_grade_entry_query()
        # query.match_source_id(gradebook_column_id, match=True)
        # query.match_date(from_, to, match=True)
        # return self._try_harder(query)"""
