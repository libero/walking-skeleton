from libero_flow.activities.archive_xml_activity import ArchiveXMLActivity
from libero_flow.activities.download_article_xml_activity import DownloadArticleXMLActivity
from libero_flow.activities.download_assets_activity import DownloadAssetsActivity
from libero_flow.activities.extract_asset_uris_activity import ExtractAssetURIsActivity
from libero_flow.activities.clone_xml_activity import CloneXMLActivity
from libero_flow.activities.generate_pdf_activity import GeneratePDFActivity


ACTIVITIES = {
    'ArchiveXMLActivity': ArchiveXMLActivity,
    'CloneXMLActivity': CloneXMLActivity,
    'DownloadArticleXMLActivity': DownloadArticleXMLActivity,
    'DownloadAssetsActivity': DownloadAssetsActivity,
    'ExtractAssetURIsActivity': ExtractAssetURIsActivity,
    'GeneratePDFActivity': GeneratePDFActivity,
}
